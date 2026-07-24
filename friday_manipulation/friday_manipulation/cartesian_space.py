# Copyright 2026 Holiday Robotics Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import math
import time
from collections.abc import Sequence

import rclpy
from rclpy.node import Node
from rclpy.time import Time
from rclpy.utilities import remove_ros_args
from ros2_interfaces_public.msg import LinkReaching, ManipulationAPI
from tf2_ros import Buffer, TransformException, TransformListener

MANIPULATION_API_TOPIC = "/hday/controller/manipulation_api"
SUBSCRIBER_WAIT_SECONDS = 5.0
POST_PUBLISH_SPIN_SECONDS = 0.5

DEFAULT_REFERENCE_FRAME = "base_link"
DEFAULT_TARGET_FRAME = "right_arm_7"
DEFAULT_TARGET_POS = (0.10, 0.0, 0.0)
DEFAULT_TARGET_QUAT = (0.0, 0.0, 0.0, 1.0)
TF_TIMEOUT_SECONDS = 5.0
RIGHT_ARM_JOINTS = [f"right_arm_{index}" for index in range(1, 8)]


def _normalize_quaternion(quaternion: Sequence[float]) -> tuple[float, float, float, float]:
    norm = math.sqrt(sum(component * component for component in quaternion))
    if norm == 0.0 or not math.isfinite(norm):
        raise ValueError("quaternion must have a finite, non-zero norm")
    x, y, z, w = quaternion
    return x / norm, y / norm, z / norm, w / norm


def _multiply_quaternions(left: Sequence[float], right: Sequence[float]) -> tuple[float, float, float, float]:
    lx, ly, lz, lw = left
    rx, ry, rz, rw = right
    return (
        lw * rx + lx * rw + ly * rz - lz * ry,
        lw * ry - lx * rz + ly * rw + lz * rx,
        lw * rz + lx * ry - ly * rx + lz * rw,
        lw * rw - lx * rx - ly * ry - lz * rz,
    )


def _parse_args(args: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Publish one Cartesian offset command for Friday.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog=(
            "Example: ros2 run friday_manipulation cartesian_space "
            "--reference-frame base_link --target-frame right_arm_7 "
            "--target-pos 0.10 0.0 0.0 --target-quat 0.0 0.0 0.0 1.0"
        ),
    )
    parser.add_argument(
        "--reference-frame",
        default=DEFAULT_REFERENCE_FRAME,
        help="frame in which the current pose and offsets are expressed",
    )
    parser.add_argument(
        "--target-frame",
        default=DEFAULT_TARGET_FRAME,
        help="end-effector frame to command",
    )
    parser.add_argument(
        "--target-pos",
        type=float,
        nargs=3,
        metavar=("X", "Y", "Z"),
        default=DEFAULT_TARGET_POS,
        help="translation offset in meters",
    )
    parser.add_argument(
        "--target-quat",
        type=float,
        nargs=4,
        metavar=("X", "Y", "Z", "W"),
        default=DEFAULT_TARGET_QUAT,
        help="rotation offset quaternion",
    )
    parsed = parser.parse_args(remove_ros_args(args=args)[1:])
    try:
        parsed.target_quat = _normalize_quaternion(parsed.target_quat)
    except ValueError as error:
        parser.error(str(error))
    return parsed


def _publish_once(node: Node, message: ManipulationAPI) -> None:
    publisher = node.create_publisher(ManipulationAPI, MANIPULATION_API_TOPIC, 10)

    deadline = time.monotonic() + SUBSCRIBER_WAIT_SECONDS
    while publisher.get_subscription_count() == 0 and time.monotonic() < deadline:
        rclpy.spin_once(node, timeout_sec=0.1)

    if publisher.get_subscription_count() == 0:
        node.get_logger().warning(f"No subscriber discovered on {MANIPULATION_API_TOPIC}; publishing anyway")

    publisher.publish(message)

    deadline = time.monotonic() + POST_PUBLISH_SPIN_SECONDS
    while time.monotonic() < deadline:
        rclpy.spin_once(node, timeout_sec=min(0.1, deadline - time.monotonic()))


def _lookup_current_transform(node: Node, buffer: Buffer, reference_frame: str, target_frame: str):
    lookup_time = Time()
    future = buffer.wait_for_transform_async(reference_frame, target_frame, lookup_time)
    rclpy.spin_until_future_complete(node, future, timeout_sec=TF_TIMEOUT_SECONDS)
    if not future.done():
        future.cancel()
        raise TransformException(f"Timed out waiting for transform {reference_frame} <- {target_frame}")
    return buffer.lookup_transform(reference_frame, target_frame, lookup_time)


def main(args: list[str] | None = None) -> int:
    cli_args = _parse_args(args)
    rclpy.init(args=args)
    node = rclpy.create_node("cartesian_space")
    buffer = Buffer()
    listener = TransformListener(buffer, node)

    try:
        try:
            transform = _lookup_current_transform(node, buffer, cli_args.reference_frame, cli_args.target_frame)
        except TransformException as error:
            node.get_logger().error(str(error))
            return 1

        translation = transform.transform.translation
        rotation = transform.transform.rotation
        current_quat = (rotation.x, rotation.y, rotation.z, rotation.w)
        target_quat = _normalize_quaternion(_multiply_quaternions(cli_args.target_quat, current_quat))

        target = LinkReaching()
        target.target_frame = cli_args.target_frame
        target.reference_frame = cli_args.reference_frame
        target.active_joints = RIGHT_ARM_JOINTS
        target.target_pos.x = translation.x + cli_args.target_pos[0]
        target.target_pos.y = translation.y + cli_args.target_pos[1]
        target.target_pos.z = translation.z + cli_args.target_pos[2]
        target.target_quat.x = target_quat[0]
        target.target_quat.y = target_quat[1]
        target.target_quat.z = target_quat[2]
        target.target_quat.w = target_quat[3]

        message = ManipulationAPI()
        message.header.stamp = node.get_clock().now().to_msg()
        message.link_reaching = [target]

        _publish_once(node, message)
        node.get_logger().info(
            f"Published {cli_args.target_frame} target at "
            f"[{target.target_pos.x:.3f}, {target.target_pos.y:.3f}, "
            f"{target.target_pos.z:.3f}] in {cli_args.reference_frame}"
        )
        return 0
    finally:
        del listener
        node.destroy_node()
        rclpy.shutdown()

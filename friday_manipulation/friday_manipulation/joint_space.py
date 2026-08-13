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
import time

import rclpy
from friday_msgs.msg import JointReaching, Manipulation
from rclpy.node import Node
from rclpy.utilities import remove_ros_args

MANIPULATION_TOPIC = "holiday/manipulation"
SUBSCRIBER_WAIT_SECONDS = 5.0
POST_PUBLISH_SPIN_SECONDS = 0.5

WAIST_JOINTS = tuple(f"waist_{index}" for index in range(1, 6))
LEFT_ARM_JOINTS = tuple(f"left_arm_{index}" for index in range(1, 8))
RIGHT_ARM_JOINTS = tuple(f"right_arm_{index}" for index in range(1, 8))
LEFT_HAND_JOINTS = tuple(f"left_hand_{finger}_{joint}" for finger in range(1, 6) for joint in range(1, 5))
RIGHT_HAND_JOINTS = tuple(f"right_hand_{finger}_{joint}" for finger in range(1, 6) for joint in range(1, 5))
HEAD_JOINTS = tuple(f"head_{index}" for index in range(1, 4))

ALL_JOINTS = WAIST_JOINTS + LEFT_ARM_JOINTS + RIGHT_ARM_JOINTS + LEFT_HAND_JOINTS + RIGHT_HAND_JOINTS + HEAD_JOINTS

READY_WAIST = (0.0, -0.48, 0.96, -0.48, 0.0)
READY_LEFT_ARM = (-0.92, 0.74, 0.0, -1.27, 0.44, 0.09, 0.0)
READY_RIGHT_ARM = (-0.92, -0.74, 0.0, -1.27, -0.44, -0.09, 0.0)


def build_joint_targets(pose: str) -> tuple[tuple[str, float], ...]:
    if pose == "init_pose":
        return tuple((joint, 0.0) for joint in ALL_JOINTS)

    ready_positions = (
        READY_WAIST
        + READY_LEFT_ARM
        + READY_RIGHT_ARM
        + (0.0,) * (len(LEFT_HAND_JOINTS) + len(RIGHT_HAND_JOINTS) + len(HEAD_JOINTS))
    )
    return tuple(zip(ALL_JOINTS, ready_positions, strict=True))


def _publish_once(node: Node, message: Manipulation) -> None:
    publisher = node.create_publisher(Manipulation, MANIPULATION_TOPIC, 1)

    deadline = time.monotonic() + SUBSCRIBER_WAIT_SECONDS
    while publisher.get_subscription_count() == 0 and time.monotonic() < deadline:
        rclpy.spin_once(node, timeout_sec=0.1)

    if publisher.get_subscription_count() == 0:
        node.get_logger().warning(f"No subscriber discovered on {MANIPULATION_TOPIC}; publishing anyway")

    publisher.publish(message)

    deadline = time.monotonic() + POST_PUBLISH_SPIN_SECONDS
    while time.monotonic() < deadline:
        rclpy.spin_once(node, timeout_sec=min(0.1, deadline - time.monotonic()))


def _parse_args(args: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Publish one predefined Friday joint-space pose.",
        epilog=(
            "Examples:\n"
            "  ros2 run friday_manipulation joint_space init_pose\n"
            "  ros2 run friday_manipulation joint_space ready_pose"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "pose",
        choices=("init_pose", "ready_pose"),
        help="init_pose commands all joints to zero; ready_pose commands the fixed ready posture",
    )
    return parser.parse_args(remove_ros_args(args=args)[1:])


def main(args: list[str] | None = None) -> int:
    cli_args = _parse_args(args)
    rclpy.init(args=args)
    node = rclpy.create_node("joint_space")

    try:
        message = Manipulation()
        message.header.stamp = node.get_clock().now().to_msg()
        message.joint_reaching = [
            JointReaching(
                target_joint=joint,
                target_position=position,
                target_velocity=0.0,
                target_acceleration=0.0,
            )
            for joint, position in build_joint_targets(cli_args.pose)
        ]

        _publish_once(node, message)
        node.get_logger().info(f"Published {cli_args.pose} with {len(message.joint_reaching)} joint targets")
        return 0
    finally:
        node.destroy_node()
        rclpy.shutdown()

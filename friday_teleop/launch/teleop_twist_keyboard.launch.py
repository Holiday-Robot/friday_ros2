from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    cmd_vel_topic = LaunchConfiguration("cmd_vel_topic")
    stamped = LaunchConfiguration("stamped")
    frame_id = LaunchConfiguration("frame_id")
    speed = LaunchConfiguration("speed")
    turn = LaunchConfiguration("turn")
    launch_prefix = LaunchConfiguration("launch_prefix")

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "cmd_vel_topic",
                default_value="/hday/controller/navigation_api",
                description="Output velocity topic",
            ),
            DeclareLaunchArgument("stamped", default_value="true", description="Publish TwistStamped messages"),
            DeclareLaunchArgument("frame_id", default_value="", description="Frame id for stamped velocity messages"),
            DeclareLaunchArgument("speed", default_value="0.03", description="Default linear speed scale"),
            DeclareLaunchArgument("turn", default_value="0.15", description="Default angular speed scale"),
            DeclareLaunchArgument(
                "launch_prefix",
                default_value='bash -c \'exec < /dev/tty; exec "$0" "$@"\'',
                description="Process prefix used to attach teleop stdin to the controlling terminal",
            ),
            Node(
                package="teleop_twist_keyboard",
                executable="teleop_twist_keyboard",
                name="teleop_twist_keyboard",
                output="screen",
                emulate_tty=True,
                prefix=launch_prefix,
                remappings=[("cmd_vel", cmd_vel_topic)],
                parameters=[
                    {
                        "stamped": ParameterValue(stamped, value_type=bool),
                        "frame_id": ParameterValue(frame_id, value_type=str),
                        "speed": ParameterValue(speed, value_type=float),
                        "turn": ParameterValue(turn, value_type=float),
                    }
                ],
            ),
        ]
    )

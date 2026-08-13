import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    use_sim_time = LaunchConfiguration("use_sim_time", default="false")
    use_joint_state_publisher_gui = LaunchConfiguration("use_joint_state_publisher_gui", default="false")
    joint_state_topic = LaunchConfiguration("joint_state_topic")

    urdf_path = os.path.join(get_package_share_directory("friday_description"), "urdf", "FM26A.urdf")
    with open(urdf_path, encoding="utf-8") as urdf_file:
        robot_description = urdf_file.read()

    params = {"robot_description": robot_description, "use_sim_time": use_sim_time}
    rviz_config_path = os.path.join(get_package_share_directory("friday_description"), "rviz", "friday.rviz")
    rviz_arguments = ["-d", rviz_config_path] if os.path.exists(rviz_config_path) else []

    return LaunchDescription(
        [
            DeclareLaunchArgument("use_sim_time", default_value="false", description="Use simulation time"),
            DeclareLaunchArgument(
                "use_joint_state_publisher_gui", default_value="false", description="Use joint state publisher GUI"
            ),
            DeclareLaunchArgument(
                "joint_state_topic",
                default_value="holiday/joint_states",
                description="Joint state topic for robot state publisher",
            ),
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                output="screen",
                parameters=[params],
                remappings=[("/joint_states", joint_state_topic)],
            ),
            Node(
                package="joint_state_publisher_gui",
                executable="joint_state_publisher_gui",
                name="joint_state_publisher",
                output="screen",
                condition=IfCondition(use_joint_state_publisher_gui),
                remappings=[("/joint_states", joint_state_topic)],
            ),
            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2",
                output="screen",
                arguments=rviz_arguments,
            ),
        ]
    )

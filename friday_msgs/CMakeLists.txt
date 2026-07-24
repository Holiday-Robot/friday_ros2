cmake_minimum_required(VERSION 3.16)
project(ros2_interfaces_public)

find_package(ament_cmake REQUIRED)
find_package(builtin_interfaces REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)

set(msg_files
  "msg/BatteryState.msg"
  "msg/EncoderState.msg"
  "msg/JointReaching.msg"
  "msg/LinkReaching.msg"
  "msg/ManipulationAPI.msg"
  "msg/MotorLimit.msg"
  "msg/MotorState.msg"
  "msg/PartSafetyState.msg"
  "msg/RobotMode.msg"
  "msg/RobotStatus.msg"
  "msg/SafetySensorState.msg"
  "msg/TactileData.msg"
  "msg/TactileLayout.msg"
  "msg/TactileMagnet.msg"
  "msg/ViewReaching.msg"
)

set(srv_files
  "srv/FaultReset.srv"
  "srv/GetBatteryState.srv"
  "srv/GetEncoderState.srv"
  "srv/GetMotorLimit.srv"
  "srv/GetMotorState.srv"
  "srv/GetRobotMode.srv"
  "srv/GetRobotStatus.srv"
  "srv/GetSafetyState.srv"
  "srv/SetJointTorqueEnable.srv"
  "srv/SetMotorLimit.srv"
  "srv/SetRobotMode.srv"
)

rosidl_generate_interfaces(${PROJECT_NAME}
  ${msg_files}
  ${srv_files}
  DEPENDENCIES builtin_interfaces geometry_msgs std_msgs
)

ament_export_dependencies(rosidl_default_runtime)

ament_package()

cmake_minimum_required(VERSION 3.16)
project(friday_msgs)

find_package(ament_cmake REQUIRED)
find_package(builtin_interfaces REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)

set(msg_files
  "msg/AvoidanceState.msg"
  "msg/BatteryPackState.msg"
  "msg/BatteryState.msg"
  "msg/BoardState.msg"
  "msg/BoardStateArray.msg"
  "msg/BumperState.msg"
  "msg/BumperStateArray.msg"
  "msg/CollisionPairState.msg"
  "msg/ControlMode.msg"
  "msg/EmergencyStop.msg"
  "msg/ExternalVideoStreamStatus.msg"
  "msg/JointLockState.msg"
  "msg/JointReaching.msg"
  "msg/LinkReaching.msg"
  "msg/LoadCellState.msg"
  "msg/LoadCellStateArray.msg"
  "msg/Manipulation.msg"
  "msg/MotorLimit.msg"
  "msg/MotorState.msg"
  "msg/MotorStateArray.msg"
  "msg/RangeState.msg"
  "msg/RangeStateArray.msg"
  "msg/TactileLayout.msg"
  "msg/TactilePointState.msg"
  "msg/TactileSensorPose.msg"
  "msg/TactileStateArray.msg"
  "msg/ViewReaching.msg"
)

set(srv_files
  "srv/GetBatteryAlarm.srv"
  "srv/GetCameraList.srv"
  "srv/GetExternalVideoStreamStatus.srv"
  "srv/GetMotorLimits.srv"
  "srv/ResetBoardFaults.srv"
  "srv/SetAvoidanceEnabled.srv"
  "srv/SetBatteryAlarm.srv"
  "srv/SetCollisionPairEnabled.srv"
  "srv/SetControlMode.srv"
  "srv/SetExternalVideoStreaming.srv"
  "srv/SetMotorCurrentLimit.srv"
  "srv/SetMotorVelocityLimit.srv"
  "srv/SetRangeSensorEnabled.srv"
)

rosidl_generate_interfaces(${PROJECT_NAME}
  ${msg_files}
  ${srv_files}
  DEPENDENCIES builtin_interfaces geometry_msgs sensor_msgs std_msgs
)

ament_export_dependencies(
  builtin_interfaces
  geometry_msgs
  rosidl_default_runtime
  sensor_msgs
  std_msgs
)

ament_package()

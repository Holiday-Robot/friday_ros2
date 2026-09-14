FROM osrf/ros:jazzy-desktop

RUN --mount=type=bind,target=/tmp/friday_ros2 \
    apt-get update \
    && apt-get install -y --no-install-recommends ros-jazzy-rmw-cyclonedds-cpp ros-jazzy-compressed-image-transport \
    && rosdep update --rosdistro jazzy \
    && rosdep install --from-paths /tmp/friday_ros2 --ignore-src --rosdistro jazzy -y \
    && rm -rf /var/lib/apt/lists/*

ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp ROS_DOMAIN_ID=138
WORKDIR /workspace
RUN chmod 1777 /workspace

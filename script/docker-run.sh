#!/usr/bin/env bash
set -euo pipefail

root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
args=()
if [[ -n "${DISPLAY:-}" && -d /tmp/.X11-unix ]]; then
    args+=(-e DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:ro)
    authority="${XAUTHORITY:-$HOME/.Xauthority}"
    if [[ -f "$authority" ]]; then
        args+=(-e XAUTHORITY=/tmp/.Xauthority -v "$authority:/tmp/.Xauthority:ro")
    fi
fi

if [[ -d /dev/dri ]]; then
    args+=(--device /dev/dri:/dev/dri)
    for device in /dev/dri/*; do
        [[ -c "$device" ]] || continue
        args+=(--group-add "$(stat -c '%g' "$device")")
    done
fi

exec docker run --rm -it --init --network host \
    --hostname "$(hostname)" \
    --user "$(id -u):$(id -g)" \
    -e HOME=/tmp \
    -e ROS_DOMAIN_ID="${ROS_DOMAIN_ID:-138}" \
    -v "$root:/workspace/src/friday_ros2" \
    "${args[@]}" "$@" friday-ros2:jazzy

#!/usr/bin/env bash
set -euo pipefail

if (( $# > 2 )); then
    printf 'Usage: %s [output_dir] [ALL|JOINT_STATES|CAMERA|LIDAR|/topic|"[JOINT_STATES, /tf]"]\n' "$0" >&2
    exit 2
fi

output_dir="${1:-/workspace/src/friday_ros2/record}"
bag_dir="${output_dir%/}/$(date +%Y%m%d_%H%M%S)"
selection="${2:-ALL}"
if [[ $selection == \[*\] ]]; then
    selection="${selection:1:-1}"
fi
item_pattern='[[:space:]]*([A-Z_]+|(/[a-zA-Z_][a-zA-Z0-9_]*)+)[[:space:]]*'
if [[ ! $selection =~ ^$item_pattern(,$item_pattern)*$ ]]; then
    printf 'Invalid selection: %s\n' "$selection" >&2
    exit 2
fi
selection="${selection//[[:space:]]/}"

IFS=, read -r -a items <<< "$selection"
patterns=()
for item in "${items[@]}"; do
    case "$item" in
        ALL)
            if (( ${#items[@]} != 1 )); then
                printf 'ALL must be used alone.\n' >&2
                exit 2
            fi
            exec ros2 bag record --storage mcap --output="$bag_dir" --all
            ;;
        JOINT_STATES) patterns+=('/holiday/joint_states') ;;
        CAMERA) patterns+=('/holiday/camera/.*') ;;
        LIDAR) patterns+=('/holiday/(lidar/.*|imu/lidar_3d_(body|mobile))') ;;
        /*) patterns+=("$item") ;;
        *)
            printf 'Unknown group: %s\n' "$item" >&2
            exit 2
            ;;
    esac
done

regex="$(IFS='|'; printf '%s' "${patterns[*]}")"
exec ros2 bag record --storage mcap --output="$bag_dir" \
    --regex "^($regex)$" --exclude-regex '/_service_event$'

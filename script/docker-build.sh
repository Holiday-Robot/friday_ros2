#!/usr/bin/env bash
set -euo pipefail

root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
exec docker build -t friday-ros2:jazzy -f "$root/docker/Dockerfile" "$@" "$root"

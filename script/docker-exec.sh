#!/usr/bin/env bash
set -euo pipefail

root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
container="$(docker ps -q --filter "volume=$root")"
if [[ -z $container || $container == *$'\n'* ]]; then
    printf 'Expected one running container mounting %s; found: %s\n' "$root" "${container:-none}" >&2
    exit 1
fi

exec docker exec -it --workdir /workspace "$container" /ros_entrypoint.sh bash

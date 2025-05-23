#!/usr/bin/env bash
set -euo pipefail

echo "→ Stopping and removing all containers, networks, volumes…"
docker compose down

echo "All services stopped."
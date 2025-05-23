#!/usr/bin/env bash
set -euo pipefail

unset DOCKER_HOST

docker context use default >/dev/null 2>&1 || true

if ! docker info >/dev/null 2>&1; then
  echo "→ Docker daemon not running, starting service…"
  sudo systemctl start docker
fi

docker compose up --build
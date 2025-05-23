#!/usr/bin/env bash
set -euo pipefail

echo "→ Unsetting any custom DOCKER_HOST"
unset DOCKER_HOST

echo "→ Ensuring Docker context is default"
docker context use default >/dev/null 2>&1 || true

echo "→ Verifying Docker daemon"
if ! docker info >/dev/null 2>&1; then
  echo "→ Docker daemon not running, starting service…"
  sudo systemctl start docker
else
  echo "→ Docker daemon is up"
fi

echo "→ Building and starting services via docker compose"
docker compose up --build

echo "All services are up!"
#!/usr/bin/env bash
set -euo pipefail
set -x

docker compose down --remove-orphans --volumes || true

if ! docker info > /dev/null 2>&1; then
  echo "→ Docker daemon not running. Starting it now…"
  if command -v systemctl > /dev/null; then
    sudo systemctl start docker
  else
    sudo service docker start
  fi
  sleep 2
fi

export DOCKER_HOST=unix:///var/run/docker.sock

docker context use default >/dev/null 2>&1 || true

cd "$(dirname "$0")"

docker compose pull
docker compose up --build -d
docker compose ps

cat <<-EOF

→ Services are up! Access them here:

  • Backend API  : http://localhost:8002
  • Frontend Dev : http://localhost:5176
  • Nginx Proxy  : http://localhost:8082
  • pgAdmin      : http://localhost:5051
  • Prometheus   : http://localhost:9092
  • Grafana      : http://localhost:3002

EOF
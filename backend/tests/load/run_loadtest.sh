#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://host.docker.internal:8000}"
OUT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT_FILE="k6-results.json"
SCRIPT="/tests/loadtest.js"

if [ -d "$OUT_DIR/$OUT_FILE" ]; then
  echo "→ removing stale directory $OUT_FILE"
  rm -rf "$OUT_DIR/$OUT_FILE"
fi

: > "$OUT_DIR/$OUT_FILE"

echo "Running load test against $BASE_URL…"
if command -v docker &>/dev/null; then
  echo "→ using Dockerized k6"
  docker run --rm \
    --add-host host.docker.internal:host-gateway \
    -u "$(id -u):$(id -g)" \
    -v "$OUT_DIR":/tests \
    -e BASE_URL="$BASE_URL" \
    grafana/k6 run \
      --vus 100 \
      --duration 5m \
      --out json=/tests/"$OUT_FILE" \
      "$SCRIPT"
elif command -v k6 &>/dev/null; then
  echo "→ using local k6"
  k6 run \
    --vus 100 \
    --duration 5m \
    --out json="$OUT_DIR/$OUT_FILE" \
    --env BASE_URL="$BASE_URL" \
    "$OUT_DIR/loadtest.js"
else
  echo "Error: neither Docker nor k6 is installed." >&2
  exit 1
fi

echo "Results written to $OUT_DIR/$OUT_FILE"
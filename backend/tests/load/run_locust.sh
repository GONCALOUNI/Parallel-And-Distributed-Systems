#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

source ../../../backend/.venv/bin/activate

locust \
  -f locustfile.py \
  --host http://localhost:8000 \
  --web-host 0.0.0.0
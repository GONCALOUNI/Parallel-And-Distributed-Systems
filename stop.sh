#!/usr/bin/env bash
set -euo pipefail
set -x

# 1. Usa o contexto do Docker Desktop
docker context use desktop-linux >/dev/null

# 2. Vai para a raiz do projecto
cd "$(dirname "$0")"

# 3. Desliga tudo
docker compose down --remove-orphans --volumes
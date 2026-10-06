#!/usr/bin/env bash
# Starts Qdrant, waits for readiness, runs search.py, tears down.
set -euo pipefail
cd "$(dirname "$0")"
trap 'docker compose down -v >/dev/null 2>&1' EXIT
docker compose up -d >/dev/null
for _ in $(seq 30); do curl -sf localhost:6333/readyz >/dev/null && break; sleep 1; done
python3 search.py

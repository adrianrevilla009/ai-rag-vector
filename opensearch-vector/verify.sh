#!/usr/bin/env bash
# Starts a single-node OpenSearch, waits for it, runs search.py, tears down.
set -euo pipefail
cd "$(dirname "$0")"
trap 'docker compose down -v >/dev/null 2>&1' EXIT
docker compose up -d >/dev/null
for _ in $(seq 60); do curl -sf localhost:9200 >/dev/null && break; sleep 2; done
python3 search.py

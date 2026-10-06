#!/usr/bin/env bash
# Starts pgvector, runs search.sql, expects the two refund rows on top, then tears down.
set -euo pipefail
cd "$(dirname "$0")"
trap 'docker compose down -v >/dev/null 2>&1' EXIT
docker compose up -d --wait >/dev/null
out=$(docker compose exec -T db psql -q -U postgres -d rag -tA -f /dev/stdin < search.sql)
echo "$out" | tail -2
[ "$(echo "$out" | tail -2 | grep -c refund)" = 2 ] && echo OK

#!/usr/bin/env bash
set -euo pipefail
url="${1:-http://localhost:8000/health}"
count="${2:-20}"
for ((i = 1; i <= count; i++)); do curl --fail --silent --show-error "$url" >/dev/null; done
echo "completed $count requests to $url"

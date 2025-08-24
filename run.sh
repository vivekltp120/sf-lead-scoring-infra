#!/usr/bin/env bash
set -euo pipefail
exec uvicorn app.main:app --host 0.0.0.0 --port 8080 --workers ${UVICORN_WORKERS:-2} --proxy-headers

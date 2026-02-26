#!/usr/bin/env bash
set -euo pipefail

PORT="${OPENCLAW_PORT:-18789}"
HOST="${OPENCLAW_HOST:-127.0.0.1}"
LOG_DIR="${HOME}/.openclaw/logs"
PID_FILE="${HOME}/.openclaw/run/gateway.pid"

mkdir -p "${LOG_DIR}"
mkdir -p "$(dirname "${PID_FILE}")"

# 如果端口已监听，认为已启动
if command -v ss >/dev/null 2>&1; then
  if ss -ltn 2>/dev/null | grep -q ":${PORT}"; then
    echo "OpenClaw gateway already listening on ${HOST}:${PORT}"
    exit 0
  fi
fi

# 如果有 PID 文件且进程存在，也认为已启动
if [[ -f "${PID_FILE}" ]]; then
  PID="$(cat "${PID_FILE}" || true)"
  if [[ -n "${PID}" ]] && kill -0 "${PID}" 2>/dev/null; then
    echo "OpenClaw gateway already running (pid ${PID})"
    exit 0
  fi
fi

echo "Starting OpenClaw gateway on ${HOST}:${PORT} (background)..."
nohup openclaw gateway --port "${PORT}" > "${LOG_DIR}/gateway.log" 2>&1 &
echo $! > "${PID_FILE}"
echo "Started pid $(cat "${PID_FILE}")"

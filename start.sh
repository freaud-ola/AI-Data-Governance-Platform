#!/usr/bin/env bash
# ==============================================================================
# AI Data Governance Platform · 一键启动脚本
#
# 同时启动 FastAPI 后端 + Vite 前端，首次运行会自动：
#   - 创建 backend/.venv 并安装依赖
#   - 复制 backend/.env.example -> backend/.env
#   - 在 frontend/ 执行 npm install
#
# 用法:
#   ./start.sh                # 本机模式：venv + uvicorn + vite（首次自动装依赖）
#   ./start.sh --backend      # 只启动后端
#   ./start.sh --frontend     # 只启动前端
#   ./start.sh --reinstall    # 强制重装前后端依赖
#   ./start.sh --docker       # Docker 模式：docker compose up（含 PG / Redis）
#   ./start.sh --docker down  # Docker 模式：docker compose down
#   ./start.sh -h | --help    # 查看帮助
#
# 环境变量:
#   BACKEND_PORT   后端端口（默认 8000）
#   FRONTEND_PORT  前端端口（默认 5173）
# ==============================================================================

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"
LOG_DIR="$ROOT_DIR/.logs"
mkdir -p "$LOG_DIR"

BACKEND_PORT="${BACKEND_PORT:-8000}"
FRONTEND_PORT="${FRONTEND_PORT:-5173}"

REINSTALL=0
RUN_BACKEND=1
RUN_FRONTEND=1
DOCKER_MODE=0
DOCKER_ACTION="up"

# ---------------- 颜色 / 日志 ----------------
if [ -t 1 ]; then
  C_BLUE="\033[0;34m"; C_GREEN="\033[0;32m"; C_YELLOW="\033[0;33m"
  C_RED="\033[0;31m"; C_DIM="\033[2m"; C_RST="\033[0m"
else
  C_BLUE=""; C_GREEN=""; C_YELLOW=""; C_RED=""; C_DIM=""; C_RST=""
fi
log()  { printf "%b[start]%b %s\n"  "$C_BLUE"   "$C_RST" "$*"; }
ok()   { printf "%b[ok]%b    %s\n"  "$C_GREEN"  "$C_RST" "$*"; }
warn() { printf "%b[warn]%b  %s\n"  "$C_YELLOW" "$C_RST" "$*"; }
err()  { printf "%b[err]%b   %s\n"  "$C_RED"    "$C_RST" "$*" >&2; }

# ---------------- 参数解析 ----------------
print_help() {
  cat <<'EOF'
AI Data Governance Platform · 一键启动脚本

两种启动模式：
  · 本机模式（默认）: venv + uvicorn + vite，开发体验最佳，前后端各自热重载
  · Docker 模式:     docker compose up，含 PostgreSQL 15 / Redis 7 基线

本机模式首次运行会自动：
  - 创建 backend/.venv 并安装依赖
  - 复制 backend/.env.example -> backend/.env
  - 在 frontend/ 执行 npm install

用法:
  ./start.sh                # 本机模式：启动前后端
  ./start.sh --backend      # 只启动后端
  ./start.sh --frontend     # 只启动前端
  ./start.sh --reinstall    # 强制重装前后端依赖
  ./start.sh --docker       # Docker 模式：docker compose up -d 全栈
  ./start.sh --docker down  # Docker 模式：docker compose down
  ./start.sh -h | --help    # 查看帮助

环境变量（本机模式）:
  BACKEND_PORT   后端端口（默认 8000）
  FRONTEND_PORT  前端端口（默认 5173）

Docker 模式的环境变量见根目录 .env.example。
EOF
}

i=0
ARGS=("$@")
while [ $i -lt ${#ARGS[@]} ]; do
  arg="${ARGS[$i]}"
  case "$arg" in
    --reinstall) REINSTALL=1 ;;
    --backend)   RUN_FRONTEND=0 ;;
    --frontend)  RUN_BACKEND=0 ;;
    --docker)
      DOCKER_MODE=1
      next_idx=$((i + 1))
      if [ $next_idx -lt ${#ARGS[@]} ]; then
        next_arg="${ARGS[$next_idx]}"
        case "$next_arg" in
          up|down|logs|ps|restart) DOCKER_ACTION="$next_arg"; i=$next_idx ;;
        esac
      fi
      ;;
    -h|--help)   print_help; exit 0 ;;
    *) err "未知参数: ${arg}"; print_help; exit 1 ;;
  esac
  i=$((i + 1))
done

# ---------------- 工具函数 ----------------
require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    err "缺少依赖命令：$1，请先安装。"
    exit 1
  fi
}

port_in_use() {
  # 仅作提示，不阻塞启动
  if command -v lsof >/dev/null 2>&1; then
    lsof -nP -iTCP:"$1" -sTCP:LISTEN >/dev/null 2>&1
  else
    return 1
  fi
}

BACKEND_PID=""
FRONTEND_PID=""
TAIL_PID=""

cleanup() {
  echo ""
  log "收到退出信号，正在关闭子进程..."
  for pid in "$TAIL_PID" "$FRONTEND_PID" "$BACKEND_PID"; do
    if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
      kill "$pid" 2>/dev/null || true
    fi
  done
  # 给 2s 优雅退出，否则强杀
  sleep 1
  for pid in "$TAIL_PID" "$FRONTEND_PID" "$BACKEND_PID"; do
    if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
      kill -9 "$pid" 2>/dev/null || true
    fi
  done
  ok "已退出"
  exit 0
}
trap cleanup INT TERM

# ---------------- 后端 ----------------
start_backend() {
  log "准备后端环境 (${BACKEND_DIR}) ..."
  require_cmd python3

  if [ ! -d "${BACKEND_DIR}/.venv" ]; then
    log "首次运行，创建虚拟环境 backend/.venv ..."
    python3 -m venv "${BACKEND_DIR}/.venv"
    REINSTALL=1
  fi

  # shellcheck source=/dev/null
  source "${BACKEND_DIR}/.venv/bin/activate"

  if [ "${REINSTALL}" = "1" ] || [ ! -f "${BACKEND_DIR}/.venv/.deps_installed" ]; then
    log "安装后端依赖 (pip install -r requirements.txt) ..."
    python -m pip install --upgrade pip >/dev/null
    python -m pip install -r "${BACKEND_DIR}/requirements.txt"
    touch "${BACKEND_DIR}/.venv/.deps_installed"
    ok "后端依赖安装完成"
  fi

  if [ ! -f "${BACKEND_DIR}/.env" ] && [ -f "${BACKEND_DIR}/.env.example" ]; then
    cp "${BACKEND_DIR}/.env.example" "${BACKEND_DIR}/.env"
    ok "已根据 .env.example 创建 backend/.env"
  fi

  if port_in_use "${BACKEND_PORT}"; then
    warn "后端端口 ${BACKEND_PORT} 已被占用，可能启动失败。可用 BACKEND_PORT=xxx ./start.sh 指定其他端口。"
  fi

  log "启动后端 uvicorn -> http://localhost:${BACKEND_PORT}/docs"
  (
    cd "${BACKEND_DIR}"
    # --reload-dir app: 只监视应用代码变更；屏蔽 .venv / tests / .logs 引发的无效重载
    exec uvicorn app.main:app --reload \
      --reload-dir app \
      --host 0.0.0.0 --port "${BACKEND_PORT}" \
      >"${LOG_DIR}/backend.log" 2>&1
  ) &
  BACKEND_PID=$!
  ok "后端已启动 (pid=${BACKEND_PID}, 日志: .logs/backend.log)"
}

# ---------------- 前端 ----------------
start_frontend() {
  log "准备前端环境 (${FRONTEND_DIR}) ..."
  require_cmd node
  require_cmd npm

  if [ "${REINSTALL}" = "1" ] || [ ! -d "${FRONTEND_DIR}/node_modules" ]; then
    log "安装前端依赖 (npm install) ..."
    (cd "${FRONTEND_DIR}" && npm install)
    ok "前端依赖安装完成"
  fi

  if port_in_use "${FRONTEND_PORT}"; then
    warn "前端端口 ${FRONTEND_PORT} 已被占用，可能启动失败。可用 FRONTEND_PORT=xxx ./start.sh 指定其他端口。"
  fi

  log "启动前端 vite -> http://localhost:${FRONTEND_PORT}"
  (
    cd "${FRONTEND_DIR}"
    # 直接 exec vite，避免 npm 包一层导致 PID 杀不掉
    exec npx --no-install vite --host --port "${FRONTEND_PORT}" \
      >"${LOG_DIR}/frontend.log" 2>&1
  ) &
  FRONTEND_PID=$!
  ok "前端已启动 (pid=${FRONTEND_PID}, 日志: .logs/frontend.log)"
}

# ---------------- Docker 模式 ----------------
run_docker() {
  require_cmd docker
  if ! docker compose version >/dev/null 2>&1; then
    err "未检测到 'docker compose'（v2 插件）。请升级 Docker Desktop / 安装 compose v2。"
    exit 1
  fi

  # daemon 健康检查：未启动时给出清晰指引，而不是抛裸错
  if ! docker info >/dev/null 2>&1; then
    err "Docker daemon 未运行或不可达。"
    echo ""
    echo "  排查与修复："
    case "$(uname -s)" in
      Darwin)
        echo "    1) 启动 Docker Desktop（约 30 秒，菜单栏图标变绿即就绪）："
        echo "         open -a Docker"
        echo "    2) 等待 'docker info' 不再报错后重试："
        echo "         until docker info >/dev/null 2>&1; do sleep 1; done && ./start.sh --docker"
        ;;
      Linux)
        echo "    1) 启动 dockerd："
        echo "         sudo systemctl start docker"
        echo "    2) 当前用户加入 docker 组以免 sudo："
        echo "         sudo usermod -aG docker \$USER && newgrp docker"
        ;;
      *)
        echo "    请确认本机 Docker Engine 已运行。"
        ;;
    esac
    echo ""
    echo "  不想用 Docker？直接用本机模式（venv + uvicorn + vite）："
    echo "         ./start.sh"
    exit 1
  fi

  if [ ! -f "${ROOT_DIR}/.env" ] && [ -f "${ROOT_DIR}/.env.example" ]; then
    cp "${ROOT_DIR}/.env.example" "${ROOT_DIR}/.env"
    ok "已根据根目录 .env.example 创建 .env"
  fi

  case "$DOCKER_ACTION" in
    up)
      log "docker compose up -d --build ..."
      (cd "${ROOT_DIR}" && docker compose up -d --build)
      echo ""
      ok "Docker 全栈已启动"
      echo "  后端 API     : http://localhost:${BACKEND_PORT}"
      echo "  Swagger UI   : http://localhost:${BACKEND_PORT}/docs"
      echo "  前端 Web     : http://localhost:${FRONTEND_PORT}"
      echo "  PostgreSQL   : localhost:5432  (db=adg user=adg)"
      echo "  Redis        : localhost:6379"
      echo ""
      echo "可选数据源栈（Hive + MySQL）：在根目录 .env 取消注释 COMPOSE_PROFILES=datasources 后执行"
      echo "  docker compose up -d"
      echo "  MySQL 映射端口见 MYSQL_PLATFORM_PORT（默认 3307）；Hive JDBC 端口见 HIVE_DEV_PORT（默认 10000）。"
      echo "  Hive：Metastore 端口 ${HIVE_METASTORE_PORT:-9083}，HS2 端口 ${HIVE_DEV_PORT:-10000}；连接请用 ./scripts/hive-beeline.sh。"
      echo ""
      echo "查看日志：docker compose logs -f backend"
      echo "停止全部：./start.sh --docker down"
      ;;
    down)
      log "docker compose down ..."
      (cd "${ROOT_DIR}" && docker compose down)
      ok "Docker 全栈已停止"
      ;;
    logs)
      (cd "${ROOT_DIR}" && exec docker compose logs -f)
      ;;
    ps)
      (cd "${ROOT_DIR}" && exec docker compose ps)
      ;;
    restart)
      (cd "${ROOT_DIR}" && docker compose restart)
      ok "Docker 全栈已重启"
      ;;
    *)
      err "不支持的 docker 子命令：${DOCKER_ACTION}"
      exit 1
      ;;
  esac
  exit 0
}

if [ "$DOCKER_MODE" = "1" ]; then
  run_docker
fi

# ---------------- 主流程（本机模式） ----------------
[ "$RUN_BACKEND"  = "1" ] && start_backend
[ "$RUN_FRONTEND" = "1" ] && start_frontend

cat <<EOF

${C_GREEN}──────────────────────────────────────────────${C_RST}
 ${C_GREEN}AI Data Governance Platform 已启动${C_RST}
${C_GREEN}──────────────────────────────────────────────${C_RST}
EOF
[ "$RUN_BACKEND"  = "1" ] && echo " 后端 API     : http://localhost:${BACKEND_PORT}"
[ "$RUN_BACKEND"  = "1" ] && echo " Swagger UI   : http://localhost:${BACKEND_PORT}/docs"
[ "$RUN_BACKEND"  = "1" ] && echo " Health Check : http://localhost:${BACKEND_PORT}/health"
[ "$RUN_FRONTEND" = "1" ] && echo " 前端 Web     : http://localhost:${FRONTEND_PORT}"
echo " 实时日志     : .logs/backend.log · .logs/frontend.log"
echo ""
echo " 按 ${C_YELLOW}Ctrl+C${C_RST} 同时停止前后端"
echo ""

# 实时打印日志（tail -F 自动跟随 logrotate / 重建文件）
LOG_FILES=()
[ "$RUN_BACKEND"  = "1" ] && LOG_FILES+=("$LOG_DIR/backend.log")
[ "$RUN_FRONTEND" = "1" ] && LOG_FILES+=("$LOG_DIR/frontend.log")

# 确保日志文件存在再 tail
for f in "${LOG_FILES[@]}"; do : > "$f"; done

tail -n 0 -F "${LOG_FILES[@]}" &
TAIL_PID=$!

# 等待任一进程退出
WAIT_PIDS=()
[ -n "$BACKEND_PID"  ] && WAIT_PIDS+=("$BACKEND_PID")
[ -n "$FRONTEND_PID" ] && WAIT_PIDS+=("$FRONTEND_PID")

# bash 3.2 (macOS 自带) 不支持 wait -n，逐个轮询
while true; do
  for pid in "${WAIT_PIDS[@]}"; do
    if ! kill -0 "$pid" 2>/dev/null; then
      err "子进程 $pid 已退出，请查看日志：.logs/"
      cleanup
    fi
  done
  sleep 2
done

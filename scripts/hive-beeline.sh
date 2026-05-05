#!/usr/bin/env bash
# 连接本地 Compose 中的 HiveServer2（默认容器 adg-hive-dev）。
#
# 不要在容器里单独执行裸命令 `hive`：会进入 Beeline 但未建立 JDBC，执行 SQL 会报
# 「No current connection」。必须带上 JDBC URL，或使用本脚本。
#
# 用法：
#   ./scripts/hive-beeline.sh                          # 交互式 Beeline
#   ./scripts/hive-beeline.sh -e 'SHOW DATABASES;'    # 执行一条 SQL 后退出
#
# 可选环境变量：HIVE_CONTAINER、HIVE_JDBC_URL
#
# SLF4J「multiple bindings」类日志可忽略。若仍 Connection refused：先看
#   docker compose logs hive-metastore hive-dev
# 确认 Metastore 已 healthy 且 HS2 已监听 10000（双容器栈见 docker-compose.yml）。

set -euo pipefail
CONTAINER="${HIVE_CONTAINER:-adg-hive-dev}"
JDBC="${HIVE_JDBC_URL:-jdbc:hive2://127.0.0.1:10000/default}"

if ! docker info >/dev/null 2>&1; then
  echo "Docker 不可用，请先启动 Docker Desktop。" >&2
  exit 1
fi
if ! docker ps --format '{{.Names}}' | grep -qx "$CONTAINER"; then
  echo "容器 ${CONTAINER} 未在运行。请先启用 COMPOSE_PROFILES=datasources 并执行 docker compose up -d。" >&2
  exit 1
fi

exec docker exec -it "$CONTAINER" beeline -u "$JDBC" "$@"

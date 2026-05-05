# 不声明 `# syntax=` frontend，避免 BuildKit 去 docker.io 拉 docker/dockerfile 镜像。
# IMAGE_REGISTRY 由 docker-compose.yml 注入，可在根 .env 中改写为国内 mirror，
# 例如：IMAGE_REGISTRY=docker.m.daocloud.io/library
#
# PIP_INDEX_URL：构建期 pip 源。默认清华 TUNA（国内常用）；海外可在根 .env 改为官方源：
#   PIP_INDEX_URL=https://pypi.org/simple
ARG IMAGE_REGISTRY=docker.io/library

FROM ${IMAGE_REGISTRY}/python:3.11-slim AS base

ARG PIP_INDEX_URL=https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_INDEX_URL=${PIP_INDEX_URL}

WORKDIR /app

# 不安装 curl：slim 镜像是 Debian，在国内 apt-get update 常因上游源超时失败。
# 健康检查直接用 Python 3 标准库的 urllib（镜像里必有 python）。

COPY requirements.txt ./
# 弱网下默认 15s 超时易导致「No matching distribution / versions: none」；加长超时与重试。
RUN pip install \
    --retries 15 \
    --default-timeout 120 \
    -r requirements.txt

COPY alembic ./alembic
COPY alembic.ini ./

COPY app ./app

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=3s --start-period=10s --retries=3 \
  CMD ["python", "-c", "import urllib.request as _u; _u.urlopen('http://127.0.0.1:8000/health', timeout=2).read()"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

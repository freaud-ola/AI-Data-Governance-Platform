# 不声明 `# syntax=` frontend，避免 BuildKit 去 docker.io 拉 docker/dockerfile 镜像。
# IMAGE_REGISTRY 由 docker-compose.yml 注入，可在根 .env 中改写为国内 mirror，
# 例如：IMAGE_REGISTRY=docker.m.daocloud.io/library
# 如果想用 RUN --mount=type=cache 的 npm 缓存，可在网络通畅时反向加回首行
# `# syntax=docker/dockerfile:1.6` 并把 `RUN npm ci` 换成 mount 形式。
ARG IMAGE_REGISTRY=docker.io/library

# ---------- Build ----------
FROM ${IMAGE_REGISTRY}/node:22-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci

COPY tsconfig.json vite.config.ts index.html ./
COPY src ./src
COPY public ./public

RUN npm run build

# ---------- Runtime ----------
FROM ${IMAGE_REGISTRY}/nginx:1.27-alpine AS runtime

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -qO- http://127.0.0.1/ >/dev/null || exit 1

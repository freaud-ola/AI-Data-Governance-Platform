# Frontend · AI Data Governance Platform

React 18 + TypeScript + Vite + Ant Design v5 + Pro Components。

## 快速启动

```bash
cd frontend
npm install
npm run dev
# 访问 http://localhost:5173
```

> 默认通过 Vite proxy 转发 `/api` 到后端 `http://localhost:8000`。请先启动后端。

## 目录结构

```
frontend/
├── src/
│   ├── api/              # axios 客户端 + 各模块 service
│   ├── components/       # 公共组件（PageHeader、ModuleStatusBanner）
│   ├── layouts/          # ProLayout 主框架
│   ├── pages/            # 各模块页面
│   │   ├── overview/     # 总览看板
│   │   ├── metadata/     # 元数据中心
│   │   ├── catalog/      # 资产目录 + 业务术语
│   │   ├── profiling/
│   │   ├── quality/      # 质量规则 + 工单
│   │   ├── lineage/
│   │   ├── standards/
│   │   ├── metrics/
│   │   ├── mdm/
│   │   ├── lifecycle/
│   │   ├── security/     # 分级分类 + 审计
│   │   ├── ai-hub/       # AI 中台 + Prompt + NL2SQL
│   │   ├── reports/
│   │   └── settings/
│   ├── routes/           # 路由 + 菜单分组
│   ├── styles/           # 全局样式
│   └── types/            # 与后端 schema 对齐的 TS 类型
└── vite.config.ts
```

## 命令

| 命令                   | 说明                                |
| ---------------------- | ----------------------------------- |
| `npm run dev`          | 开发模式（HMR）                     |
| `npm run build`        | 生产构建（含 tsc 检查）             |
| `npm run preview`      | 本地预览构建产物                    |
| `npm run typecheck`    | 单独跑 `tsc --noEmit`               |
| `npm run lint`         | ESLint（仅 fail on errors）         |
| `npm run lint:strict`  | ESLint，0 warning 即 fail（CI 用）  |
| `npm run lint:fix`     | ESLint 自动修复                     |
| `npm run format`       | Prettier 全量格式化                 |
| `npm run format:check` | Prettier 仅校验，不写入             |

## 全局错误处理

- **路由内异常** → `<ErrorBoundary>` 兜底（在 `MainLayout` 内包裹 `<Outlet>`），保留左侧菜单，仅内容区降级。
- **请求异常** → axios 拦截器把 `success === false` 的业务错误也抛成 reject；TanStack Query 的 `QueryCache.onError` / `MutationCache.onError` 统一抓取，调用全局 `toast.error()`。
- **手动反馈** → 任意非 React 模块都可以 `import { toast, notify } from '@/utils/feedback'` 弹消息，AntD `<App>` 内部桥负责把 `message` / `notification` 实例注入。
- **静默 query** → 在 `useQuery({ meta: { silent: true } })` 中显式声明，可跳过自动 toast（用于轮询）。

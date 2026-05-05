import {
  ApartmentOutlined,
  ApiOutlined,
  AuditOutlined,
  BarChartOutlined,
  BookOutlined,
  ClusterOutlined,
  CodeSandboxOutlined,
  DashboardOutlined,
  DatabaseOutlined,
  ExperimentOutlined,
  FileTextOutlined,
  FundProjectionScreenOutlined,
  HddOutlined,
  RobotOutlined,
  SafetyCertificateOutlined,
  SearchOutlined,
  SettingOutlined,
  SnippetsOutlined,
  TagsOutlined,
} from '@ant-design/icons';
import type { ReactNode } from 'react';

import AIHubPage from '@/pages/ai-hub/AIHub';
import NL2SQLPlayground from '@/pages/ai-hub/NL2SQLPlayground';
import PromptRegistry from '@/pages/ai-hub/PromptRegistry';
import CatalogPage from '@/pages/catalog/Catalog';
import GlossaryPage from '@/pages/catalog/Glossary';
import LifecyclePage from '@/pages/lifecycle/Lifecycle';
import LineagePage from '@/pages/lineage/Lineage';
import MDMPage from '@/pages/mdm/MDM';
import MetadataPage from '@/pages/metadata/Metadata';
import MetricsPage from '@/pages/metrics/Metrics';
import OverviewPage from '@/pages/overview/Overview';
import ProfilingPage from '@/pages/profiling/Profiling';
import IncidentsPage from '@/pages/quality/Incidents';
import QualityPage from '@/pages/quality/Quality';
import ReportsPage from '@/pages/reports/Reports';
import AuditPage from '@/pages/security/Audit';
import SecurityPage from '@/pages/security/Security';
import SettingsPage from '@/pages/settings/Settings';
import StandardsPage from '@/pages/standards/Standards';

export interface AppRoute {
  path: string;
  name: string;
  icon?: ReactNode;
  element: ReactNode;
  /** 在菜单中隐藏 */
  hideInMenu?: boolean;
  children?: AppRoute[];
}

export const ROUTES: AppRoute[] = [
  {
    path: '/overview',
    name: '总览看板',
    icon: <DashboardOutlined />,
    element: <OverviewPage />,
  },
  {
    path: '/metadata',
    name: '元数据中心',
    icon: <DatabaseOutlined />,
    element: <MetadataPage />,
  },
  {
    path: '/catalog',
    name: '资产目录',
    icon: <SearchOutlined />,
    element: <CatalogPage />,
  },
  {
    path: '/glossary',
    name: '业务术语',
    icon: <BookOutlined />,
    element: <GlossaryPage />,
  },
  {
    path: '/profiling',
    name: '数据探查',
    icon: <ExperimentOutlined />,
    element: <ProfilingPage />,
  },
  {
    path: '/quality',
    name: '数据质量',
    icon: <SafetyCertificateOutlined />,
    element: <QualityPage />,
  },
  {
    path: '/quality/incidents',
    name: '质量工单',
    icon: <SnippetsOutlined />,
    element: <IncidentsPage />,
  },
  {
    path: '/lineage',
    name: '数据血缘',
    icon: <ApartmentOutlined />,
    element: <LineagePage />,
  },
  {
    path: '/standards',
    name: '数据标准',
    icon: <TagsOutlined />,
    element: <StandardsPage />,
  },
  {
    path: '/metrics',
    name: '指标管理',
    icon: <BarChartOutlined />,
    element: <MetricsPage />,
  },
  {
    path: '/mdm',
    name: '主数据',
    icon: <ClusterOutlined />,
    element: <MDMPage />,
  },
  {
    path: '/lifecycle',
    name: '生命周期',
    icon: <HddOutlined />,
    element: <LifecyclePage />,
  },
  {
    path: '/security',
    name: '数据安全',
    icon: <SafetyCertificateOutlined />,
    element: <SecurityPage />,
  },
  {
    path: '/security/audit',
    name: '审计日志',
    icon: <AuditOutlined />,
    element: <AuditPage />,
  },
  {
    path: '/ai-hub',
    name: 'AI 能力中台',
    icon: <RobotOutlined />,
    element: <AIHubPage />,
  },
  {
    path: '/ai-hub/prompt',
    name: 'Prompt 管理',
    icon: <CodeSandboxOutlined />,
    element: <PromptRegistry />,
  },
  {
    path: '/ai-hub/nl2sql',
    name: 'NL2SQL Playground',
    icon: <ApiOutlined />,
    element: <NL2SQLPlayground />,
  },
  {
    path: '/reports',
    name: '报告中心',
    icon: <FileTextOutlined />,
    element: <ReportsPage />,
  },
  {
    path: '/settings',
    name: '系统设置',
    icon: <SettingOutlined />,
    element: <SettingsPage />,
  },
];

/** 顶层菜单分组（用于 ProLayout） */
export interface MenuGroup {
  key: string;
  name: string;
  icon: ReactNode;
  children: { path: string; name: string; icon?: ReactNode }[];
}

export const MENU_GROUPS: MenuGroup[] = [
  {
    key: 'overview',
    name: '总览',
    icon: <DashboardOutlined />,
    children: [{ path: '/overview', name: '总览看板', icon: <DashboardOutlined /> }],
  },
  {
    key: 'metadata',
    name: '元数据与目录',
    icon: <DatabaseOutlined />,
    children: [
      { path: '/metadata', name: '数据源 / Schema', icon: <DatabaseOutlined /> },
      { path: '/catalog', name: '资产目录', icon: <SearchOutlined /> },
      { path: '/glossary', name: '业务术语', icon: <BookOutlined /> },
      { path: '/profiling', name: '数据探查', icon: <ExperimentOutlined /> },
    ],
  },
  {
    key: 'quality',
    name: '质量与血缘',
    icon: <SafetyCertificateOutlined />,
    children: [
      { path: '/quality', name: '质量规则', icon: <SafetyCertificateOutlined /> },
      { path: '/quality/incidents', name: '质量工单', icon: <SnippetsOutlined /> },
      { path: '/lineage', name: '数据血缘', icon: <ApartmentOutlined /> },
    ],
  },
  {
    key: 'governance',
    name: '建模治理',
    icon: <FundProjectionScreenOutlined />,
    children: [
      { path: '/standards', name: '数据标准', icon: <TagsOutlined /> },
      { path: '/metrics', name: '指标管理', icon: <BarChartOutlined /> },
      { path: '/mdm', name: '主数据', icon: <ClusterOutlined /> },
      { path: '/lifecycle', name: '生命周期 / 成本', icon: <HddOutlined /> },
    ],
  },
  {
    key: 'security',
    name: '安全与合规',
    icon: <SafetyCertificateOutlined />,
    children: [
      { path: '/security', name: '分级分类 / 脱敏', icon: <SafetyCertificateOutlined /> },
      { path: '/security/audit', name: '审计日志', icon: <AuditOutlined /> },
    ],
  },
  {
    key: 'ai',
    name: 'AI 能力中台',
    icon: <RobotOutlined />,
    children: [
      { path: '/ai-hub', name: 'AI 总览', icon: <RobotOutlined /> },
      { path: '/ai-hub/prompt', name: 'Prompt 管理', icon: <CodeSandboxOutlined /> },
      { path: '/ai-hub/nl2sql', name: 'NL2SQL', icon: <ApiOutlined /> },
    ],
  },
  {
    key: 'system',
    name: '报告与系统',
    icon: <SettingOutlined />,
    children: [
      { path: '/reports', name: '报告中心', icon: <FileTextOutlined /> },
      { path: '/settings', name: '系统设置', icon: <SettingOutlined /> },
    ],
  },
];

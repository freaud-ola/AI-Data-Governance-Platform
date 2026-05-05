import { apiClient, ApiResponse, PageData } from '@/api/client';
import type {
  AIInvocation,
  AIPrompt,
  DataAsset,
  DataSource,
  DataStandard,
  DomainCoverage,
  LifecyclePolicy,
  LineageGraph,
  MasterEntity,
  Metric,
  OverviewKPI,
  QualityIncident,
  QualityRule,
  ReportItem,
  SecurityClassification,
  TimePoint,
} from '@/types/api';

const unwrap = async <T>(p: Promise<{ data: ApiResponse<T> }>): Promise<T> => {
  const resp = await p;
  if (!resp.data.success) {
    throw new Error(resp.data.message || 'API error');
  }
  return resp.data.data;
};

export const overviewApi = {
  kpi: () => unwrap<OverviewKPI>(apiClient.get('/overview/kpi')),
  qualityTrend: () => unwrap<TimePoint[]>(apiClient.get('/overview/trend/quality')),
  lineageTrend: () => unwrap<TimePoint[]>(apiClient.get('/overview/trend/lineage')),
  assetTrend: () => unwrap<TimePoint[]>(apiClient.get('/overview/trend/asset')),
  domainCoverage: () => unwrap<DomainCoverage[]>(apiClient.get('/overview/domain-coverage')),
};

export const metadataApi = {
  listSources: () => unwrap<DataSource[]>(apiClient.get('/metadata/sources')),
};

export const catalogApi = {
  listAssets: (params?: {
    keyword?: string;
    domain?: string;
    layer?: string;
    page?: number;
    page_size?: number;
  }) => unwrap<PageData<DataAsset>>(apiClient.get('/catalog/assets', { params })),
  getAsset: (id: string) => unwrap<DataAsset>(apiClient.get(`/catalog/assets/${id}`)),
};

export const qualityApi = {
  listRules: () => unwrap<QualityRule[]>(apiClient.get('/quality/rules')),
  listIncidents: () => unwrap<QualityIncident[]>(apiClient.get('/quality/incidents')),
};

export const lineageApi = {
  getGraph: () => unwrap<LineageGraph>(apiClient.get('/lineage/graph')),
};

export const standardsApi = {
  list: () => unwrap<DataStandard[]>(apiClient.get('/standards')),
};

export const metricsApi = {
  list: () => unwrap<Metric[]>(apiClient.get('/metrics')),
};

export const mdmApi = {
  listEntities: () => unwrap<MasterEntity[]>(apiClient.get('/mdm/entities')),
};

export const lifecycleApi = {
  listPolicies: () => unwrap<LifecyclePolicy[]>(apiClient.get('/lifecycle/policies')),
};

export const securityApi = {
  listClassifications: () =>
    unwrap<SecurityClassification[]>(apiClient.get('/security/classifications')),
};

export const aiHubApi = {
  listPrompts: () => unwrap<AIPrompt[]>(apiClient.get('/ai/prompts')),
  listInvocations: () => unwrap<AIInvocation[]>(apiClient.get('/ai/invocations')),
};

export const reportsApi = {
  list: () => unwrap<ReportItem[]>(apiClient.get('/reports')),
};

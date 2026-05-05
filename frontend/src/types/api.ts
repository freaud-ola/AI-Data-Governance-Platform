/**
 * 与后端 Pydantic Schema 对齐的 TypeScript 类型。
 * 当后端 schema 变化时，同步更新本文件。
 */

export interface DataSource {
  id: string;
  name: string;
  type: string;
  status: 'online' | 'offline' | 'error';
  table_count: number;
  last_sync_at: string | null;
  description: string | null;
  /** 宿主机或文档约定的接入主机（容器内需换用 Compose 服务名） */
  endpoint_host?: string | null;
  endpoint_port?: number | null;
  default_database?: string | null;
}

export interface DataAsset {
  id: string;
  name: string;
  full_name: string;
  source_id: string;
  source_type: string;
  database: string;
  schema: string;
  layer: string;
  owner: string;
  domain: string;
  row_count: number;
  size_bytes: number;
  quality_score: number;
  pii_level: string;
  tags: string[];
  description: string | null;
  ai_description: string | null;
  updated_at: string;
}

export interface QualityRule {
  id: string;
  name: string;
  dimension: string;
  asset_id: string;
  asset_name: string;
  expression: string;
  severity: string;
  enabled: boolean;
  last_run_status: string;
  last_run_at: string | null;
}

export interface QualityIncident {
  id: string;
  rule_id: string;
  rule_name: string;
  asset_name: string;
  severity: string;
  status: string;
  owner: string;
  created_at: string;
  resolved_at: string | null;
}

export interface LineageNode {
  id: string;
  name: string;
  type: 'table' | 'job' | 'column';
  layer: string | null;
}

export interface LineageEdge {
  source: string;
  target: string;
  relation: string;
}

export interface LineageGraph {
  nodes: LineageNode[];
  edges: LineageEdge[];
}

export interface DataStandard {
  id: string;
  code: string;
  name: string;
  category: string;
  data_type: string;
  bound_count: number;
  owner: string;
  status: string;
}

export interface Metric {
  id: string;
  code: string;
  name: string;
  domain: string;
  formula: string;
  owner: string;
  version: string;
  status: string;
}

export interface MasterEntity {
  id: string;
  name: string;
  type: string;
  record_count: number;
  owner: string;
  last_merge_at: string | null;
}

export interface LifecyclePolicy {
  id: string;
  name: string;
  asset_pattern: string;
  cold_after_days: number;
  archive_after_days: number;
  delete_after_days: number | null;
  enabled: boolean;
}

export interface SecurityClassification {
  asset_id: string;
  asset_name: string;
  classification: string;
  pii_level: string;
  masking_strategy: string | null;
  owner: string;
}

export interface AIPrompt {
  id: string;
  name: string;
  scenario: string;
  version: string;
  status: string;
  avg_tokens: number;
  success_rate: number;
}

export interface AIInvocation {
  id: string;
  scenario: string;
  model: string;
  tokens: number;
  cost: number;
  latency_ms: number;
  status: string;
  created_at: string;
}

export interface OverviewKPI {
  asset_total: number;
  asset_today_new: number;
  quality_score: number;
  quality_incidents_open: number;
  pii_assets: number;
  coverage_lineage: number;
  coverage_comment: number;
  ai_invocations_today: number;
  ai_cost_today: number;
}

export interface TimePoint {
  ts: string;
  value: number;
}

export interface DomainCoverage {
  domain: string;
  asset_count: number;
  quality_score: number;
  governance_score: number;
}

export interface ReportItem {
  id: string;
  name: string;
  type: string;
  period: string;
  status: string;
  generated_at: string;
}

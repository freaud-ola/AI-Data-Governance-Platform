import { useQuery } from '@tanstack/react-query';
import { Card, Col, Row, Spin, Table, Tag } from 'antd';

import ModuleStatusBanner from '@/components/ModuleStatusBanner';
import PageHeader from '@/components/PageHeader';
import { lineageApi } from '@/api/services';
import type { LineageNode } from '@/types/api';

const NODE_TYPE_COLOR: Record<string, string> = {
  table: 'blue',
  job: 'purple',
  column: 'cyan',
};

const LAYER_COLOR: Record<string, string> = {
  ODS: 'default',
  DWD: 'blue',
  DWS: 'cyan',
  ADS: 'magenta',
};

function Lineage() {
  const { data, isLoading } = useQuery({
    queryKey: ['lineage-graph'],
    queryFn: lineageApi.getGraph,
  });

  return (
    <div>
      <PageHeader
        title="数据血缘"
        subtitle="任务 / 表 / 字段三级血缘 — 静态解析 (sqlglot) + 运行时 Hook 双轨制 (OpenLineage)"
        tags={[
          { color: 'blue', text: 'P1' },
          { color: 'orange', text: 'Phase 3' },
        ]}
      />
      <ModuleStatusBanner stage="mvp-skeleton" arch="02-数据质量与血缘 §血缘双轨" />

      <Row gutter={16}>
        <Col span={16}>
          <Card title="血缘图（占位 — 后续接入 AntV G6）" variant="outlined">
            <Spin spinning={isLoading}>
              <div
                style={{
                  height: 420,
                  position: 'relative',
                  background: 'repeating-linear-gradient(45deg, #fafafa 0 20px, #f0f2f5 20px 40px)',
                  borderRadius: 8,
                  padding: 16,
                  overflow: 'auto',
                }}
              >
                <pre style={{ fontSize: 12, color: 'rgba(0,0,0,0.65)', margin: 0 }}>
                  {JSON.stringify(data ?? { nodes: [], edges: [] }, null, 2)}
                </pre>
              </div>
            </Spin>
          </Card>
        </Col>
        <Col span={8}>
          <Card title="血缘节点" variant="outlined">
            <Table<LineageNode>
              rowKey="id"
              size="small"
              pagination={false}
              loading={isLoading}
              dataSource={data?.nodes ?? []}
              columns={[
                { title: '节点', dataIndex: 'name' },
                {
                  title: '类型',
                  dataIndex: 'type',
                  width: 80,
                  render: (t: string) => <Tag color={NODE_TYPE_COLOR[t] ?? 'default'}>{t}</Tag>,
                },
                {
                  title: '层',
                  dataIndex: 'layer',
                  width: 70,
                  render: (l: string | null) =>
                    l ? <Tag color={LAYER_COLOR[l] ?? 'default'}>{l}</Tag> : '-',
                },
              ]}
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
}

export default Lineage;

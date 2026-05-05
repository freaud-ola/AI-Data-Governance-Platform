import { useQuery } from '@tanstack/react-query';
import { Card, Col, Row, Statistic, Table, Tag } from 'antd';

import ModuleStatusBanner from '@/components/ModuleStatusBanner';
import PageHeader from '@/components/PageHeader';
import { securityApi } from '@/api/services';

const PII_COLOR: Record<string, string> = {
  L1: 'green',
  L2: 'blue',
  L3: 'orange',
  L4: 'red',
};

const CLS_COLOR: Record<string, string> = {
  public: 'green',
  internal: 'blue',
  confidential: 'orange',
  strict: 'red',
};

function Security() {
  const { data, isLoading } = useQuery({
    queryKey: ['security-classifications'],
    queryFn: securityApi.listClassifications,
  });

  return (
    <div>
      <PageHeader
        title="数据安全"
        subtitle="分级分类 / 静态 + 动态脱敏 / RBAC + ABAC / 个保法 / GDPR"
        tags={[{ color: 'red', text: 'P0' }]}
      />
      <ModuleStatusBanner stage="mvp-skeleton" arch="04-安全与合规" />

      <Row gutter={16} style={{ marginBottom: 16 }}>
        <Col span={6}>
          <Card variant="outlined">
            <Statistic title="L4 严格保密" value={32} valueStyle={{ color: '#cf1322' }} />
          </Card>
        </Col>
        <Col span={6}>
          <Card variant="outlined">
            <Statistic title="L3 机密" value={68} valueStyle={{ color: '#fa8c16' }} />
          </Card>
        </Col>
        <Col span={6}>
          <Card variant="outlined">
            <Statistic title="L2 内部" value={1242} />
          </Card>
        </Col>
        <Col span={6}>
          <Card variant="outlined">
            <Statistic title="脱敏策略生效" value={184} suffix="个字段" />
          </Card>
        </Col>
      </Row>

      <Card title="资产分级 / 脱敏配置" variant="outlined">
        <Table
          rowKey="asset_id"
          loading={isLoading}
          dataSource={data ?? []}
          pagination={false}
          columns={[
            { title: '资产', dataIndex: 'asset_name' },
            {
              title: '分类',
              dataIndex: 'classification',
              width: 130,
              render: (c: string) => <Tag color={CLS_COLOR[c] ?? 'default'}>{c}</Tag>,
            },
            {
              title: 'PII',
              dataIndex: 'pii_level',
              width: 70,
              render: (l: string) => <Tag color={PII_COLOR[l] ?? 'default'}>{l}</Tag>,
            },
            {
              title: '脱敏策略',
              dataIndex: 'masking_strategy',
              render: (v: string | null) =>
                v ?? <span style={{ color: 'rgba(0,0,0,0.45)' }}>未启用</span>,
            },
            { title: '负责人', dataIndex: 'owner', width: 130 },
          ]}
        />
      </Card>
    </div>
  );
}

export default Security;

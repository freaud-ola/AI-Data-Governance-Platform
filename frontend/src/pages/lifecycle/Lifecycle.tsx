import { useQuery } from '@tanstack/react-query';
import { Card, Col, Row, Statistic, Switch, Table, Tag } from 'antd';

import ModuleStatusBanner from '@/components/ModuleStatusBanner';
import PageHeader from '@/components/PageHeader';
import { lifecycleApi } from '@/api/services';

function Lifecycle() {
  const { data, isLoading } = useQuery({
    queryKey: ['lifecycle-policies'],
    queryFn: lifecycleApi.listPolicies,
  });

  return (
    <div>
      <PageHeader
        title="生命周期 / 成本"
        subtitle="冷热分层 / TTL / 资产 ROI — 与调度元数据 + 存储 API 联动"
        tags={[{ color: 'gold', text: 'P2' }]}
      />
      <ModuleStatusBanner stage="mvp-skeleton" arch="01-元数据接入与建模 §生命周期" />

      <Row gutter={16} style={{ marginBottom: 16 }}>
        <Col span={6}>
          <Card variant="outlined">
            <Statistic title="冷数据占比" value={28.4} suffix="%" precision={1} />
          </Card>
        </Col>
        <Col span={6}>
          <Card variant="outlined">
            <Statistic title="本月节省存储" value="1.8 TB" />
          </Card>
        </Col>
        <Col span={6}>
          <Card variant="outlined">
            <Statistic title="低活资产" value={142} valueStyle={{ color: '#fa8c16' }} />
          </Card>
        </Col>
        <Col span={6}>
          <Card variant="outlined">
            <Statistic title="月度成本（估算）" value="$ 18,420" />
          </Card>
        </Col>
      </Row>

      <Card title="生命周期策略" variant="outlined">
        <Table
          rowKey="id"
          loading={isLoading}
          dataSource={data ?? []}
          pagination={false}
          columns={[
            { title: '策略名', dataIndex: 'name', width: 200 },
            {
              title: '匹配规则',
              dataIndex: 'asset_pattern',
              render: (v: string) => <code>{v}</code>,
            },
            {
              title: '冷却天数',
              dataIndex: 'cold_after_days',
              width: 100,
              align: 'right',
              render: (v: number) => <Tag color="blue">{v}d</Tag>,
            },
            {
              title: '归档天数',
              dataIndex: 'archive_after_days',
              width: 100,
              align: 'right',
              render: (v: number) => <Tag color="orange">{v}d</Tag>,
            },
            {
              title: '删除天数',
              dataIndex: 'delete_after_days',
              width: 100,
              align: 'right',
              render: (v: number | null) => (v ? <Tag color="red">{v}d</Tag> : '-'),
            },
            {
              title: '启用',
              dataIndex: 'enabled',
              width: 80,
              render: (v: boolean) => <Switch checked={v} size="small" />,
            },
          ]}
        />
      </Card>
    </div>
  );
}

export default Lifecycle;

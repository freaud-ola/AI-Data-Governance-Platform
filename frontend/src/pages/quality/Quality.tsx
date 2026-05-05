import { PlayCircleOutlined, PlusOutlined } from '@ant-design/icons';
import { useQuery } from '@tanstack/react-query';
import { Badge, Button, Card, Space, Switch, Table, Tag } from 'antd';
import dayjs from 'dayjs';

import ModuleStatusBanner from '@/components/ModuleStatusBanner';
import PageHeader from '@/components/PageHeader';
import { qualityApi } from '@/api/services';
import type { QualityRule } from '@/types/api';

const DIM_COLOR: Record<string, string> = {
  completeness: 'blue',
  uniqueness: 'cyan',
  validity: 'purple',
  consistency: 'magenta',
  accuracy: 'gold',
  timeliness: 'orange',
  integrity: 'volcano',
};

const STATUS_MAP: Record<
  string,
  { color: 'success' | 'error' | 'default' | 'warning'; text: string }
> = {
  passed: { color: 'success', text: '通过' },
  failed: { color: 'error', text: '失败' },
  pending: { color: 'default', text: '未执行' },
};

function Quality() {
  const { data, isLoading } = useQuery({
    queryKey: ['quality-rules'],
    queryFn: qualityApi.listRules,
  });

  return (
    <div>
      <PageHeader
        title="数据质量"
        subtitle="7 维度规则编排 / SLA / 漂移检测 — 基于 Great Expectations + Soda Core"
        tags={[{ color: 'red', text: 'P0' }]}
        extra={
          <Space>
            <Button icon={<PlayCircleOutlined />}>批量执行</Button>
            <Button type="primary" icon={<PlusOutlined />}>
              新建规则
            </Button>
          </Space>
        }
      />
      <ModuleStatusBanner stage="mvp-skeleton" arch="02-数据质量与血缘 §质量规则" />

      <Card title="质量规则列表" variant="outlined">
        <Table<QualityRule>
          rowKey="id"
          loading={isLoading}
          dataSource={data ?? []}
          pagination={false}
          columns={[
            { title: '规则名', dataIndex: 'name', width: 200 },
            { title: '资产', dataIndex: 'asset_name' },
            {
              title: '维度',
              dataIndex: 'dimension',
              width: 130,
              render: (d: string) => <Tag color={DIM_COLOR[d] ?? 'default'}>{d}</Tag>,
            },
            {
              title: '严重等级',
              dataIndex: 'severity',
              width: 90,
              render: (s: string) => (
                <Tag color={s === 'P0' ? 'red' : s === 'P1' ? 'orange' : 'blue'}>{s}</Tag>
              ),
            },
            {
              title: '表达式',
              dataIndex: 'expression',
              ellipsis: true,
              render: (v: string) => <code style={{ fontSize: 12 }}>{v}</code>,
            },
            {
              title: '状态',
              dataIndex: 'enabled',
              width: 90,
              render: (v: boolean) => <Switch checked={v} size="small" />,
            },
            {
              title: '上次执行',
              dataIndex: 'last_run_status',
              width: 110,
              render: (s: string) => {
                const m = STATUS_MAP[s] ?? { color: 'default' as const, text: s };
                return <Badge status={m.color} text={m.text} />;
              },
            },
            {
              title: '执行时间',
              dataIndex: 'last_run_at',
              width: 150,
              render: (t: string | null) => (t ? dayjs(t).format('MM-DD HH:mm') : '-'),
            },
          ]}
        />
      </Card>
    </div>
  );
}

export default Quality;

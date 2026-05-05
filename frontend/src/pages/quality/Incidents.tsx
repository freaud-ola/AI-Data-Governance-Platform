import { useQuery } from '@tanstack/react-query';
import { Button, Card, Space, Table, Tag } from 'antd';
import dayjs from 'dayjs';

import ModuleStatusBanner from '@/components/ModuleStatusBanner';
import PageHeader from '@/components/PageHeader';
import { qualityApi } from '@/api/services';

function Incidents() {
  const { data, isLoading } = useQuery({
    queryKey: ['quality-incidents-page'],
    queryFn: qualityApi.listIncidents,
  });

  const STATUS_COLOR: Record<string, string> = {
    open: 'red',
    processing: 'orange',
    resolved: 'green',
    closed: 'default',
  };

  return (
    <div>
      <PageHeader
        title="质量工单"
        subtitle="工单闭环：发现 → 分派 → 整改 → 关闭 — Phase 3 上线 Temporal 工作流"
        tags={[{ color: 'orange', text: 'Phase 3' }]}
      />
      <ModuleStatusBanner stage="mvp-skeleton" arch="02-数据质量与血缘 §工单闭环" />

      <Card variant="outlined">
        <Table
          rowKey="id"
          loading={isLoading}
          dataSource={data ?? []}
          pagination={false}
          columns={[
            { title: '工单号', dataIndex: 'id', width: 160 },
            { title: '规则', dataIndex: 'rule_name' },
            { title: '资产', dataIndex: 'asset_name' },
            {
              title: '严重',
              dataIndex: 'severity',
              width: 80,
              render: (s: string) => (
                <Tag color={s === 'P0' ? 'red' : s === 'P1' ? 'orange' : 'blue'}>{s}</Tag>
              ),
            },
            {
              title: '状态',
              dataIndex: 'status',
              width: 100,
              render: (s: string) => <Tag color={STATUS_COLOR[s] ?? 'default'}>{s}</Tag>,
            },
            { title: '负责人', dataIndex: 'owner', width: 120 },
            {
              title: '创建时间',
              dataIndex: 'created_at',
              width: 170,
              render: (t: string) => dayjs(t).format('YYYY-MM-DD HH:mm'),
            },
            {
              title: '操作',
              width: 150,
              render: () => (
                <Space>
                  <Button type="link" size="small">
                    查看
                  </Button>
                  <Button type="link" size="small">
                    流转
                  </Button>
                </Space>
              ),
            },
          ]}
        />
      </Card>
    </div>
  );
}

export default Incidents;

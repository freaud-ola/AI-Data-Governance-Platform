import { useQuery } from '@tanstack/react-query';
import { Card, Table, Tag } from 'antd';
import dayjs from 'dayjs';

import ModuleStatusBanner from '@/components/ModuleStatusBanner';
import PageHeader from '@/components/PageHeader';
import { reportsApi } from '@/api/services';

function Reports() {
  const { data, isLoading } = useQuery({ queryKey: ['reports'], queryFn: reportsApi.list });

  return (
    <div>
      <PageHeader
        title="报告中心"
        subtitle="治理日报 / 数据健康 / 合规导出 / DSAR — 模板化 + Agent 自动生成"
        tags={[{ color: 'gold', text: 'P2' }]}
      />
      <ModuleStatusBanner stage="mvp-skeleton" arch="06-开发路线图与风险 §Phase 5" />

      <Card variant="outlined">
        <Table
          rowKey="id"
          loading={isLoading}
          dataSource={data ?? []}
          pagination={false}
          columns={[
            { title: '报告', dataIndex: 'name' },
            {
              title: '类型',
              dataIndex: 'type',
              width: 110,
              render: (v: string) => <Tag color="blue">{v}</Tag>,
            },
            { title: '周期', dataIndex: 'period', width: 130 },
            {
              title: '状态',
              dataIndex: 'status',
              width: 110,
              render: (s: string) => {
                const map: Record<string, string> = {
                  published: 'green',
                  archived: 'default',
                  draft: 'orange',
                };
                return <Tag color={map[s] ?? 'default'}>{s}</Tag>;
              },
            },
            {
              title: '生成时间',
              dataIndex: 'generated_at',
              width: 180,
              render: (t: string) => dayjs(t).format('YYYY-MM-DD HH:mm'),
            },
          ]}
        />
      </Card>
    </div>
  );
}

export default Reports;

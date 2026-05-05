import { useQuery } from '@tanstack/react-query';
import { Card, Table, Tag } from 'antd';

import ModuleStatusBanner from '@/components/ModuleStatusBanner';
import PageHeader from '@/components/PageHeader';
import { metricsApi } from '@/api/services';

function Metrics() {
  const { data, isLoading } = useQuery({ queryKey: ['metrics'], queryFn: metricsApi.list });

  return (
    <div>
      <PageHeader
        title="指标管理"
        subtitle="指标定义 / 口径 / 版本 / 一致性校验 — 与 dbt-metrics 兼容"
        tags={[{ color: 'cyan', text: 'P1' }]}
      />
      <ModuleStatusBanner stage="mvp-skeleton" arch="01-元数据接入与建模 §指标管理" />

      <Card variant="outlined">
        <Table
          rowKey="id"
          loading={isLoading}
          dataSource={data ?? []}
          pagination={false}
          columns={[
            {
              title: '指标编码',
              dataIndex: 'code',
              width: 100,
              render: (v: string) => <Tag color="blue">{v}</Tag>,
            },
            { title: '名称', dataIndex: 'name', width: 180 },
            { title: '业务域', dataIndex: 'domain', width: 100 },
            { title: '口径', dataIndex: 'formula', render: (v: string) => <code>{v}</code> },
            { title: 'Owner', dataIndex: 'owner', width: 130 },
            { title: '版本', dataIndex: 'version', width: 80 },
            {
              title: '状态',
              dataIndex: 'status',
              width: 110,
              render: (s: string) => {
                const map: Record<string, string> = {
                  online: 'green',
                  approved: 'blue',
                  draft: 'default',
                  deprecated: 'red',
                };
                return <Tag color={map[s] ?? 'default'}>{s}</Tag>;
              },
            },
          ]}
        />
      </Card>
    </div>
  );
}

export default Metrics;

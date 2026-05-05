import { useQuery } from '@tanstack/react-query';
import { Card, Table, Tag } from 'antd';

import ModuleStatusBanner from '@/components/ModuleStatusBanner';
import PageHeader from '@/components/PageHeader';
import { standardsApi } from '@/api/services';

function Standards() {
  const { data, isLoading } = useQuery({ queryKey: ['standards'], queryFn: standardsApi.list });

  return (
    <div>
      <PageHeader
        title="数据标准"
        subtitle="字段标准 / 码值表 / 命名规范 / AI 推荐绑定 — Phase 5 完成"
        tags={[
          { color: 'cyan', text: 'P1' },
          { color: 'gold', text: 'Phase 5' },
        ]}
      />
      <ModuleStatusBanner stage="mvp-skeleton" arch="01-元数据接入与建模 §数据标准" />

      <Card variant="outlined">
        <Table
          rowKey="id"
          loading={isLoading}
          dataSource={data ?? []}
          pagination={false}
          columns={[
            {
              title: '标准编码',
              dataIndex: 'code',
              width: 180,
              render: (v: string) => <code>{v}</code>,
            },
            { title: '名称', dataIndex: 'name' },
            { title: '类别', dataIndex: 'category', width: 120 },
            {
              title: '数据类型',
              dataIndex: 'data_type',
              width: 160,
              render: (v: string) => <code>{v}</code>,
            },
            {
              title: '已绑定字段',
              dataIndex: 'bound_count',
              width: 130,
              align: 'right',
              render: (v: number) => <Tag color={v > 100 ? 'green' : 'blue'}>{v}</Tag>,
            },
            { title: '负责人', dataIndex: 'owner', width: 130 },
            {
              title: '状态',
              dataIndex: 'status',
              width: 100,
              render: (s: string) => (
                <Tag color={s === 'published' ? 'green' : s === 'draft' ? 'default' : 'orange'}>
                  {s}
                </Tag>
              ),
            },
          ]}
        />
      </Card>
    </div>
  );
}

export default Standards;

import { useQuery } from '@tanstack/react-query';
import { Card, Table, Tag } from 'antd';
import dayjs from 'dayjs';

import ModuleStatusBanner from '@/components/ModuleStatusBanner';
import PageHeader from '@/components/PageHeader';
import { mdmApi } from '@/api/services';

function MDM() {
  const { data, isLoading } = useQuery({
    queryKey: ['mdm-entities'],
    queryFn: mdmApi.listEntities,
  });

  return (
    <div>
      <PageHeader
        title="主数据 (MDM)"
        subtitle="实体注册 / 黄金记录 / 同义词归并 — AI 辅助实体匹配"
        tags={[{ color: 'gold', text: 'P2' }]}
      />
      <ModuleStatusBanner stage="mvp-skeleton" arch="01-元数据接入与建模 §主数据" />

      <Card variant="outlined">
        <Table
          rowKey="id"
          loading={isLoading}
          dataSource={data ?? []}
          pagination={false}
          columns={[
            { title: '实体名', dataIndex: 'name' },
            {
              title: '类型',
              dataIndex: 'type',
              width: 120,
              render: (t: string) => <Tag color={t === 'party' ? 'blue' : 'purple'}>{t}</Tag>,
            },
            {
              title: '记录数',
              dataIndex: 'record_count',
              width: 160,
              align: 'right',
              render: (v: number) => v.toLocaleString(),
            },
            { title: 'Owner', dataIndex: 'owner', width: 130 },
            {
              title: '上次合并',
              dataIndex: 'last_merge_at',
              width: 180,
              render: (t: string | null) => (t ? dayjs(t).format('YYYY-MM-DD HH:mm') : '-'),
            },
          ]}
        />
      </Card>
    </div>
  );
}

export default MDM;

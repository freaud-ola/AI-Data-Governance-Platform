import { useQuery } from '@tanstack/react-query';
import { Card, Progress, Table, Tag } from 'antd';

import ModuleStatusBanner from '@/components/ModuleStatusBanner';
import PageHeader from '@/components/PageHeader';
import { aiHubApi } from '@/api/services';

const STATUS_MAP: Record<string, string> = {
  online: 'green',
  staging: 'orange',
  draft: 'default',
};

function PromptRegistry() {
  const { data, isLoading } = useQuery({
    queryKey: ['ai-prompts-page'],
    queryFn: aiHubApi.listPrompts,
  });

  return (
    <div>
      <PageHeader
        title="Prompt 管理"
        subtitle="Prompt Registry / 版本管理 / 灰度发布 / 评测 — 集成 Langfuse"
        tags={[{ color: 'purple', text: 'P0' }]}
      />
      <ModuleStatusBanner stage="mvp-skeleton" arch="03-AI能力层设计 §Prompt 治理" />

      <Card variant="outlined">
        <Table
          rowKey="id"
          loading={isLoading}
          dataSource={data ?? []}
          pagination={false}
          columns={[
            { title: 'Prompt 名称', dataIndex: 'name' },
            {
              title: '场景',
              dataIndex: 'scenario',
              width: 130,
              render: (s: string) => <Tag color="blue">{s}</Tag>,
            },
            { title: '版本', dataIndex: 'version', width: 80 },
            {
              title: '状态',
              dataIndex: 'status',
              width: 110,
              render: (s: string) => <Tag color={STATUS_MAP[s] ?? 'default'}>{s}</Tag>,
            },
            { title: '平均 Token', dataIndex: 'avg_tokens', width: 130, align: 'right' },
            {
              title: '成功率',
              dataIndex: 'success_rate',
              width: 200,
              render: (v: number) => <Progress percent={Math.round(v * 100)} />,
            },
          ]}
        />
      </Card>
    </div>
  );
}

export default PromptRegistry;

import { CheckCircleTwoTone, CloseCircleTwoTone, RobotOutlined } from '@ant-design/icons';
import { useQuery } from '@tanstack/react-query';
import { Card, Col, Progress, Row, Space, Statistic, Table, Tag, Typography } from 'antd';
import dayjs from 'dayjs';

import ModuleStatusBanner from '@/components/ModuleStatusBanner';
import PageHeader from '@/components/PageHeader';
import { aiHubApi, overviewApi } from '@/api/services';

const { Text } = Typography;

const STATUS_MAP: Record<string, string> = {
  online: 'green',
  staging: 'orange',
  draft: 'default',
};

function AIHub() {
  const kpiQuery = useQuery({ queryKey: ['ai-overview-kpi'], queryFn: overviewApi.kpi });
  const promptsQ = useQuery({ queryKey: ['ai-prompts'], queryFn: aiHubApi.listPrompts });
  const invQ = useQuery({ queryKey: ['ai-invocations'], queryFn: aiHubApi.listInvocations });

  const successRate = invQ.data
    ? invQ.data.filter((i) => i.status === 'success').length / Math.max(invQ.data.length, 1)
    : 0;

  return (
    <div>
      <PageHeader
        title="AI 能力中台"
        subtitle="LLM Router / Prompt 治理 / Agent + MCP / RAG / LLMOps — 项目核心差异化"
        tags={[
          { color: 'purple', text: 'P0' },
          { color: 'blue', text: 'AI Native' },
        ]}
      />
      <ModuleStatusBanner stage="mvp-skeleton" arch="03-AI能力层设计" />

      <Row gutter={16} style={{ marginBottom: 16 }}>
        <Col span={6}>
          <Card variant="outlined">
            <Statistic
              title="今日调用"
              value={kpiQuery.data?.ai_invocations_today ?? 0}
              prefix={<RobotOutlined />}
            />
            <Text type="secondary">私有部署 + 外网 Fallback</Text>
          </Card>
        </Col>
        <Col span={6}>
          <Card variant="outlined">
            <Statistic
              title="今日成本"
              prefix="$"
              precision={2}
              value={kpiQuery.data?.ai_cost_today ?? 0}
            />
            <Text type="secondary">Token 计费 + 缓存命中</Text>
          </Card>
        </Col>
        <Col span={6}>
          <Card variant="outlined">
            <Statistic
              title="成功率（近100次）"
              value={(successRate * 100).toFixed(1)}
              suffix="%"
            />
            <Progress percent={Math.round(successRate * 100)} size="small" showInfo={false} />
          </Card>
        </Col>
        <Col span={6}>
          <Card variant="outlined">
            <Statistic
              title="活跃 Prompt"
              value={promptsQ.data?.filter((p) => p.status === 'online').length ?? 0}
            />
            <Text type="secondary">线上 / 灰度 / 草稿三态管理</Text>
          </Card>
        </Col>
      </Row>

      <Row gutter={16}>
        <Col span={12}>
          <Card title="Prompt Registry" variant="outlined">
            <Table
              rowKey="id"
              size="small"
              loading={promptsQ.isLoading}
              dataSource={promptsQ.data ?? []}
              pagination={false}
              columns={[
                { title: '名称', dataIndex: 'name' },
                {
                  title: '场景',
                  dataIndex: 'scenario',
                  width: 110,
                  render: (s: string) => <Tag color="blue">{s}</Tag>,
                },
                { title: '版本', dataIndex: 'version', width: 80 },
                {
                  title: '状态',
                  dataIndex: 'status',
                  width: 90,
                  render: (s: string) => <Tag color={STATUS_MAP[s] ?? 'default'}>{s}</Tag>,
                },
                {
                  title: '成功率',
                  dataIndex: 'success_rate',
                  width: 110,
                  render: (v: number) => <Progress percent={Math.round(v * 100)} size="small" />,
                },
              ]}
            />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="近期 LLM 调用" variant="outlined">
            <Table
              rowKey="id"
              size="small"
              loading={invQ.isLoading}
              dataSource={invQ.data ?? []}
              pagination={false}
              columns={[
                {
                  title: '场景',
                  dataIndex: 'scenario',
                  width: 110,
                  render: (s: string) => <Tag color="purple">{s}</Tag>,
                },
                { title: '模型', dataIndex: 'model' },
                { title: 'Tokens', dataIndex: 'tokens', width: 90, align: 'right' },
                { title: '耗时(ms)', dataIndex: 'latency_ms', width: 110, align: 'right' },
                {
                  title: '$',
                  dataIndex: 'cost',
                  width: 80,
                  align: 'right',
                  render: (v: number) => v.toFixed(3),
                },
                {
                  title: '状态',
                  dataIndex: 'status',
                  width: 80,
                  render: (s: string) =>
                    s === 'success' ? (
                      <Space size={4}>
                        <CheckCircleTwoTone twoToneColor="#52c41a" /> {s}
                      </Space>
                    ) : (
                      <Space size={4}>
                        <CloseCircleTwoTone twoToneColor="#cf1322" /> {s}
                      </Space>
                    ),
                },
                {
                  title: '时间',
                  dataIndex: 'created_at',
                  width: 90,
                  render: (t: string) => dayjs(t).format('HH:mm:ss'),
                },
              ]}
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
}

export default AIHub;

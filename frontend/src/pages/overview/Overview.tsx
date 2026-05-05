import {
  ApartmentOutlined,
  ArrowUpOutlined,
  DatabaseOutlined,
  DollarCircleOutlined,
  RobotOutlined,
  SafetyCertificateOutlined,
  WarningOutlined,
} from '@ant-design/icons';
import { Area, Column } from '@ant-design/plots';
import { useQuery } from '@tanstack/react-query';
import {
  Card,
  Col,
  Empty,
  Progress,
  Row,
  Space,
  Spin,
  Statistic,
  Table,
  Tag,
  Typography,
} from 'antd';

import ModuleStatusBanner from '@/components/ModuleStatusBanner';
import PageHeader from '@/components/PageHeader';
import { overviewApi, qualityApi } from '@/api/services';
import type { DomainCoverage } from '@/types/api';

const { Text } = Typography;

function Overview() {
  const kpiQuery = useQuery({ queryKey: ['overview-kpi'], queryFn: overviewApi.kpi });
  const qualityTrend = useQuery({ queryKey: ['quality-trend'], queryFn: overviewApi.qualityTrend });
  const assetTrend = useQuery({ queryKey: ['asset-trend'], queryFn: overviewApi.assetTrend });
  const lineageTrend = useQuery({ queryKey: ['lineage-trend'], queryFn: overviewApi.lineageTrend });
  const domainCoverage = useQuery({
    queryKey: ['domain-coverage'],
    queryFn: overviewApi.domainCoverage,
  });
  const incidents = useQuery({
    queryKey: ['quality-incidents'],
    queryFn: qualityApi.listIncidents,
  });

  const kpi = kpiQuery.data;

  return (
    <div>
      <PageHeader
        title="总览看板"
        subtitle="全局数据治理健康度，覆盖资产、质量、血缘、安全、AI 五大维度"
        tags={[
          { color: 'blue', text: 'P0 模块' },
          { color: 'green', text: 'MVP 已上线' },
        ]}
      />
      <ModuleStatusBanner
        stage="mvp-skeleton"
        arch="00-总体规划-v2 §五"
        arch_link="../../doc/Architecture/00-总体规划-v2.md"
      />

      <Spin spinning={kpiQuery.isLoading}>
        <Row gutter={[16, 16]}>
          <Col xs={24} sm={12} lg={6}>
            <Card variant="outlined">
              <Statistic
                title="资产总数"
                value={kpi?.asset_total ?? 0}
                prefix={<DatabaseOutlined />}
                suffix={
                  <Text type="success" style={{ fontSize: 14 }}>
                    <ArrowUpOutlined /> {kpi?.asset_today_new ?? 0}
                  </Text>
                }
              />
              <Text type="secondary">较昨日新增</Text>
            </Card>
          </Col>
          <Col xs={24} sm={12} lg={6}>
            <Card variant="outlined">
              <Statistic
                title="数据质量分"
                value={kpi?.quality_score ?? 0}
                suffix="/100"
                prefix={<SafetyCertificateOutlined />}
                precision={1}
                valueStyle={{ color: '#3f8600' }}
              />
              <Text type="secondary">7 维度加权得分</Text>
            </Card>
          </Col>
          <Col xs={24} sm={12} lg={6}>
            <Card variant="outlined">
              <Statistic
                title="待处理质量工单"
                value={kpi?.quality_incidents_open ?? 0}
                prefix={<WarningOutlined />}
                valueStyle={{ color: '#cf1322' }}
              />
              <Text type="secondary">P0/P1 优先处理</Text>
            </Card>
          </Col>
          <Col xs={24} sm={12} lg={6}>
            <Card variant="outlined">
              <Statistic
                title="今日 AI 调用"
                value={kpi?.ai_invocations_today ?? 0}
                prefix={<RobotOutlined />}
              />
              <Text type="secondary">
                成本 <DollarCircleOutlined /> ${kpi?.ai_cost_today.toFixed(2) ?? '0.00'}
              </Text>
            </Card>
          </Col>
        </Row>

        <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
          <Col xs={24} sm={12} lg={6}>
            <Card title="血缘覆盖率" variant="outlined">
              <Progress
                percent={kpi ? Math.round(kpi.coverage_lineage * 100) : 0}
                strokeColor={{ from: '#108ee9', to: '#722ed1' }}
              />
              <Text type="secondary">表级 + 字段级合并，目标 ≥85%</Text>
            </Card>
          </Col>
          <Col xs={24} sm={12} lg={6}>
            <Card title="字段注释覆盖率" variant="outlined">
              <Progress
                percent={kpi ? Math.round(kpi.coverage_comment * 100) : 0}
                strokeColor={{ from: '#13c2c2', to: '#52c41a' }}
              />
              <Text type="secondary">AI 注释 + 人工审核</Text>
            </Card>
          </Col>
          <Col xs={24} sm={12} lg={6}>
            <Card title="敏感资产" variant="outlined">
              <Statistic value={kpi?.pii_assets ?? 0} prefix={<SafetyCertificateOutlined />} />
              <Text type="secondary">含 L3 / L4 个人信息字段</Text>
            </Card>
          </Col>
          <Col xs={24} sm={12} lg={6}>
            <Card title="血缘节点" variant="outlined">
              <Statistic
                value={kpi?.coverage_lineage ? Math.round(kpi.coverage_lineage * 1000) : 0}
                prefix={<ApartmentOutlined />}
              />
              <Text type="secondary">已采集任务/表/字段三级</Text>
            </Card>
          </Col>
        </Row>
      </Spin>

      <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
        <Col xs={24} lg={16}>
          <Card title="数据质量趋势（近 14 天）" variant="outlined">
            <Spin spinning={qualityTrend.isLoading}>
              {qualityTrend.data && qualityTrend.data.length > 0 ? (
                <Area
                  data={qualityTrend.data}
                  xField="ts"
                  yField="value"
                  height={260}
                  shapeField="smooth"
                  style={{ fill: '#1677ff', fillOpacity: 0.45 }}
                />
              ) : (
                <Empty />
              )}
            </Spin>
          </Card>
        </Col>
        <Col xs={24} lg={8}>
          <Card title="资产增长" variant="outlined">
            <Spin spinning={assetTrend.isLoading}>
              {assetTrend.data && assetTrend.data.length > 0 ? (
                <Column
                  data={assetTrend.data}
                  xField="ts"
                  yField="value"
                  height={260}
                  style={{ fill: '#722ed1' }}
                />
              ) : (
                <Empty />
              )}
            </Spin>
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
        <Col xs={24} lg={12}>
          <Card title="业务域治理覆盖" variant="outlined">
            <Spin spinning={domainCoverage.isLoading}>
              <Table<DomainCoverage>
                rowKey="domain"
                size="small"
                pagination={false}
                dataSource={domainCoverage.data ?? []}
                columns={[
                  { title: '业务域', dataIndex: 'domain' },
                  { title: '资产数', dataIndex: 'asset_count', align: 'right' },
                  {
                    title: '质量分',
                    dataIndex: 'quality_score',
                    align: 'right',
                    render: (v: number) => (
                      <Tag color={v >= 90 ? 'green' : v >= 80 ? 'blue' : 'orange'}>
                        {v.toFixed(1)}
                      </Tag>
                    ),
                  },
                  {
                    title: '治理分',
                    dataIndex: 'governance_score',
                    align: 'right',
                    render: (v: number) => (
                      <Progress percent={Math.round(v)} size="small" style={{ width: 120 }} />
                    ),
                  },
                ]}
              />
            </Spin>
          </Card>
        </Col>
        <Col xs={24} lg={12}>
          <Card title="最新质量事件" variant="outlined">
            <Spin spinning={incidents.isLoading}>
              <Table
                rowKey="id"
                size="small"
                pagination={false}
                dataSource={incidents.data ?? []}
                columns={[
                  { title: '工单号', dataIndex: 'id', width: 130 },
                  { title: '规则', dataIndex: 'rule_name' },
                  {
                    title: '严重',
                    dataIndex: 'severity',
                    width: 70,
                    render: (s: string) => (
                      <Tag color={s === 'P0' ? 'red' : s === 'P1' ? 'orange' : 'blue'}>{s}</Tag>
                    ),
                  },
                  {
                    title: '状态',
                    dataIndex: 'status',
                    width: 90,
                    render: (s: string) => {
                      const map: Record<string, string> = {
                        open: 'red',
                        processing: 'orange',
                        resolved: 'green',
                        closed: 'default',
                      };
                      return <Tag color={map[s] ?? 'default'}>{s}</Tag>;
                    },
                  },
                  { title: '负责人', dataIndex: 'owner', width: 110 },
                ]}
              />
            </Spin>
          </Card>
        </Col>
      </Row>

      <Row style={{ marginTop: 16 }}>
        <Col span={24}>
          <Card variant="outlined" size="small">
            <Space split={<Tag>·</Tag>}>
              <span>
                📚 架构文档：
                <a href="https://github.com/" target="_blank" rel="noreferrer">
                  v2 总体规划
                </a>
              </span>
              <span>🔌 数据接入：Hive 集群 + 数据平台 MySQL（2 类）</span>
              <span>🤖 AI 模型：4 类场景在线</span>
              <span>
                📊 血缘趋势：{lineageTrend.data?.[lineageTrend.data.length - 1]?.value ?? '-'}%
              </span>
            </Space>
          </Card>
        </Col>
      </Row>
    </div>
  );
}

export default Overview;

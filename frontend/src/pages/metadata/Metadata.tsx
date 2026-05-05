import { ApiOutlined, CloudSyncOutlined, PlusOutlined, ReloadOutlined } from '@ant-design/icons';
import { useQuery } from '@tanstack/react-query';
import { Badge, Button, Card, Col, Row, Space, Table, Tag, Tooltip } from 'antd';
import dayjs from 'dayjs';

import ModuleStatusBanner from '@/components/ModuleStatusBanner';
import PageHeader from '@/components/PageHeader';
import { metadataApi } from '@/api/services';
import type { DataSource } from '@/types/api';

const TYPE_TAG: Record<string, string> = {
  hive: 'volcano',
  mysql: 'blue',
  iceberg: 'cyan',
  dbt: 'purple',
  scheduler: 'gold',
};

const STATUS_BADGE: Record<string, 'success' | 'error' | 'warning' | 'default'> = {
  online: 'success',
  error: 'error',
  offline: 'default',
};

function Metadata() {
  const { data, isLoading, refetch } = useQuery({
    queryKey: ['metadata-sources'],
    queryFn: metadataApi.listSources,
  });

  const onlineCount = data?.filter((d) => d.status === 'online').length ?? 0;
  const errorCount = data?.filter((d) => d.status === 'error').length ?? 0;
  const totalTables = data?.reduce((sum, d) => sum + d.table_count, 0) ?? 0;

  return (
    <div>
      <PageHeader
        title="元数据中心"
        subtitle="当前对齐两类数据源：Hive 集群 + 数据平台 MySQL；Docker profile datasources 提供本地实例"
        tags={[{ color: 'blue', text: 'P0 模块' }]}
        extra={
          <Space>
            <Button icon={<ReloadOutlined />} onClick={() => refetch()}>
              刷新
            </Button>
            <Button type="primary" icon={<PlusOutlined />}>
              新增数据源
            </Button>
          </Space>
        }
      />
      <ModuleStatusBanner stage="mvp-skeleton" arch="01-元数据接入与建模 · Docker mysql-platform / hive-dev" />

      <Row gutter={16} style={{ marginBottom: 16 }}>
        <Col span={6}>
          <Card variant="outlined">
            <Space direction="vertical" size={2}>
              <span style={{ color: 'rgba(0,0,0,0.45)' }}>已接入数据源</span>
              <span style={{ fontSize: 22, fontWeight: 600 }}>{data?.length ?? 0}</span>
            </Space>
          </Card>
        </Col>
        <Col span={6}>
          <Card variant="outlined">
            <Space direction="vertical" size={2}>
              <span style={{ color: 'rgba(0,0,0,0.45)' }}>在线数据源</span>
              <span style={{ fontSize: 22, fontWeight: 600, color: '#3f8600' }}>{onlineCount}</span>
            </Space>
          </Card>
        </Col>
        <Col span={6}>
          <Card variant="outlined">
            <Space direction="vertical" size={2}>
              <span style={{ color: 'rgba(0,0,0,0.45)' }}>异常数据源</span>
              <span style={{ fontSize: 22, fontWeight: 600, color: '#cf1322' }}>{errorCount}</span>
            </Space>
          </Card>
        </Col>
        <Col span={6}>
          <Card variant="outlined">
            <Space direction="vertical" size={2}>
              <span style={{ color: 'rgba(0,0,0,0.45)' }}>累计表数</span>
              <span style={{ fontSize: 22, fontWeight: 600 }}>{totalTables.toLocaleString()}</span>
            </Space>
          </Card>
        </Col>
      </Row>

      <Card title="数据源列表" variant="outlined">
        <Table<DataSource>
          rowKey="id"
          loading={isLoading}
          dataSource={data ?? []}
          pagination={false}
          columns={[
            {
              title: '名称',
              dataIndex: 'name',
              render: (v, row) => (
                <a>
                  {v}
                  <div style={{ color: 'rgba(0,0,0,0.45)', fontSize: 12 }}>{row.id}</div>
                </a>
              ),
            },
            {
              title: '类型',
              dataIndex: 'type',
              width: 100,
              render: (t: string) => <Tag color={TYPE_TAG[t] ?? 'default'}>{t.toUpperCase()}</Tag>,
            },
            {
              title: '接入地址',
              key: 'endpoint',
              width: 160,
              render: (_: unknown, row: DataSource) => {
                const host = row.endpoint_host;
                const port = row.endpoint_port;
                if (host && typeof port === 'number') {
                  return (
                    <span style={{ fontFamily: 'monospace', fontSize: 13 }}>
                      {host}:{port}
                    </span>
                  );
                }
                return '—';
              },
            },
            {
              title: '默认库',
              dataIndex: 'default_database',
              width: 130,
              ellipsis: true,
              render: (v: string | null) => v ?? '—',
            },
            {
              title: '状态',
              dataIndex: 'status',
              width: 110,
              render: (s: string) => <Badge status={STATUS_BADGE[s] ?? 'default'} text={s} />,
            },
            { title: '表数量', dataIndex: 'table_count', width: 100, align: 'right' },
            {
              title: '最近同步',
              dataIndex: 'last_sync_at',
              width: 180,
              render: (t: string | null) => (t ? dayjs(t).format('YYYY-MM-DD HH:mm') : '-'),
            },
            { title: '说明', dataIndex: 'description', ellipsis: true },
            {
              title: '操作',
              width: 200,
              render: () => (
                <Space>
                  <Tooltip title="同步">
                    <Button type="link" size="small" icon={<CloudSyncOutlined />}>
                      同步
                    </Button>
                  </Tooltip>
                  <Tooltip title="测试连接">
                    <Button type="link" size="small" icon={<ApiOutlined />}>
                      连通性
                    </Button>
                  </Tooltip>
                </Space>
              ),
            },
          ]}
        />
      </Card>
    </div>
  );
}

export default Metadata;

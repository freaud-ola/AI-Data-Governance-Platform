import { RobotOutlined, SearchOutlined } from '@ant-design/icons';
import { useQuery } from '@tanstack/react-query';
import { Card, Input, Select, Space, Table, Tag, Tooltip, Typography } from 'antd';
import dayjs from 'dayjs';
import { useState } from 'react';

import ModuleStatusBanner from '@/components/ModuleStatusBanner';
import PageHeader from '@/components/PageHeader';
import { catalogApi } from '@/api/services';
import type { DataAsset } from '@/types/api';

const { Text, Paragraph } = Typography;

const LAYER_COLOR: Record<string, string> = {
  ODS: 'default',
  DWD: 'blue',
  DWS: 'cyan',
  ADS: 'magenta',
};

const PII_COLOR: Record<string, string> = {
  L1: 'green',
  L2: 'blue',
  L3: 'orange',
  L4: 'red',
};

function Catalog() {
  const [keyword, setKeyword] = useState('');
  const [domain, setDomain] = useState<string | undefined>();
  const [layer, setLayer] = useState<string | undefined>();
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);

  const { data, isLoading } = useQuery({
    queryKey: ['catalog-assets', keyword, domain, layer, page, pageSize],
    queryFn: () =>
      catalogApi.listAssets({
        keyword: keyword || undefined,
        domain,
        layer,
        page,
        page_size: pageSize,
      }),
  });

  return (
    <div>
      <PageHeader
        title="资产目录"
        subtitle="全文检索 / 业务域筛选 / AI 自动注释 — Phase 2 接入语义搜索 (RAG + 向量库)"
        tags={[
          { color: 'blue', text: 'P0' },
          { color: 'green', text: 'AI 增强' },
        ]}
      />
      <ModuleStatusBanner stage="mvp-skeleton" arch="01-元数据接入与建模 §资产目录" />

      <Card variant="outlined" style={{ marginBottom: 16 }}>
        <Space wrap>
          <Input.Search
            placeholder="搜索表名 / 描述 / 负责人"
            allowClear
            style={{ width: 320 }}
            prefix={<SearchOutlined />}
            onSearch={(v) => {
              setPage(1);
              setKeyword(v);
            }}
          />
          <Select
            placeholder="业务域"
            allowClear
            style={{ width: 160 }}
            value={domain}
            onChange={(v) => {
              setPage(1);
              setDomain(v);
            }}
            options={[
              { label: '交易', value: '交易' },
              { label: '用户', value: '用户' },
              { label: '营销', value: '营销' },
              { label: '风控', value: '风控' },
              { label: '财务', value: '财务' },
              { label: '供应链', value: '供应链' },
            ]}
          />
          <Select
            placeholder="数仓分层"
            allowClear
            style={{ width: 160 }}
            value={layer}
            onChange={(v) => {
              setPage(1);
              setLayer(v);
            }}
            options={['ODS', 'DWD', 'DWS', 'ADS'].map((l) => ({ label: l, value: l }))}
          />
        </Space>
      </Card>

      <Card variant="outlined">
        <Table<DataAsset>
          rowKey="id"
          loading={isLoading}
          dataSource={data?.items ?? []}
          pagination={{
            current: page,
            pageSize,
            total: data?.meta.total ?? 0,
            showTotal: (t) => `共 ${t} 条`,
            onChange: (p, ps) => {
              setPage(p);
              setPageSize(ps);
            },
          }}
          columns={[
            {
              title: '表名',
              dataIndex: 'name',
              width: 260,
              render: (v: string, row) => (
                <div>
                  <a style={{ fontWeight: 600 }}>{v}</a>
                  <div style={{ color: 'rgba(0,0,0,0.45)', fontSize: 12 }}>{row.full_name}</div>
                </div>
              ),
            },
            {
              title: '分层',
              dataIndex: 'layer',
              width: 80,
              render: (l: string) => <Tag color={LAYER_COLOR[l] ?? 'default'}>{l}</Tag>,
            },
            {
              title: '业务域',
              dataIndex: 'domain',
              width: 90,
            },
            {
              title: 'Owner',
              dataIndex: 'owner',
              width: 120,
            },
            {
              title: '质量分',
              dataIndex: 'quality_score',
              width: 90,
              align: 'right',
              render: (v: number) => (
                <Tag color={v >= 90 ? 'green' : v >= 80 ? 'blue' : 'orange'}>{v.toFixed(1)}</Tag>
              ),
            },
            {
              title: 'PII',
              dataIndex: 'pii_level',
              width: 70,
              render: (l: string) => <Tag color={PII_COLOR[l] ?? 'default'}>{l}</Tag>,
            },
            {
              title: '描述 / AI 注释',
              dataIndex: 'description',
              ellipsis: { showTitle: false },
              render: (_v: string, row) => (
                <Tooltip title={row.description ?? row.ai_description ?? ''}>
                  <div>
                    {row.description ? (
                      <Text>{row.description}</Text>
                    ) : (
                      <Paragraph style={{ margin: 0 }} type="secondary" ellipsis>
                        <RobotOutlined style={{ color: '#722ed1' }} /> {row.ai_description}
                      </Paragraph>
                    )}
                  </div>
                </Tooltip>
              ),
            },
            {
              title: '更新时间',
              dataIndex: 'updated_at',
              width: 150,
              render: (t: string) => dayjs(t).format('YYYY-MM-DD HH:mm'),
            },
          ]}
        />
      </Card>
    </div>
  );
}

export default Catalog;

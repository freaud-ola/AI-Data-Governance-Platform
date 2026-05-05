import { Card, Col, Descriptions, Row, Tabs, Tag } from 'antd';

import ModuleStatusBanner from '@/components/ModuleStatusBanner';
import PageHeader from '@/components/PageHeader';

function Settings() {
  return (
    <div>
      <PageHeader
        title="系统设置"
        subtitle="租户 / 用户 / SSO / 配置中心 / LLM Provider — Phase 1 雏形"
        tags={[{ color: 'blue', text: 'P0' }]}
      />
      <ModuleStatusBanner stage="mvp-skeleton" arch="05-部署与运维" />

      <Tabs
        items={[
          {
            key: 'tenant',
            label: '租户与用户',
            children: (
              <Row gutter={16}>
                <Col span={12}>
                  <Card title="当前租户" variant="outlined">
                    <Descriptions column={1} size="small">
                      <Descriptions.Item label="租户 ID">
                        <code>default</code>
                      </Descriptions.Item>
                      <Descriptions.Item label="名称">默认租户</Descriptions.Item>
                      <Descriptions.Item label="状态">
                        <Tag color="green">active</Tag>
                      </Descriptions.Item>
                      <Descriptions.Item label="创建时间">2026-04-28 22:00:00</Descriptions.Item>
                    </Descriptions>
                  </Card>
                </Col>
                <Col span={12}>
                  <Card title="SSO" variant="outlined">
                    <Descriptions column={1} size="small">
                      <Descriptions.Item label="协议">OIDC (Keycloak)</Descriptions.Item>
                      <Descriptions.Item label="客户端 ID">
                        <code>data-governance</code>
                      </Descriptions.Item>
                      <Descriptions.Item label="状态">
                        <Tag color="orange">未接入（MVP）</Tag>
                      </Descriptions.Item>
                    </Descriptions>
                  </Card>
                </Col>
              </Row>
            ),
          },
          {
            key: 'llm',
            label: 'LLM Provider',
            children: (
              <Card variant="outlined">
                <Descriptions column={2} size="small" bordered>
                  <Descriptions.Item label="默认模型 (注释)">
                    qwen2.5-32b（私有部署）
                  </Descriptions.Item>
                  <Descriptions.Item label="默认模型 (NL2SQL)">deepseek-coder-v2</Descriptions.Item>
                  <Descriptions.Item label="协议">OpenAI 兼容</Descriptions.Item>
                  <Descriptions.Item label="敏感扫描">默认开启</Descriptions.Item>
                  <Descriptions.Item label="月度配额">$ 5,000</Descriptions.Item>
                  <Descriptions.Item label="语义缓存">启用 (Redis)</Descriptions.Item>
                </Descriptions>
              </Card>
            ),
          },
          {
            key: 'connectors',
            label: '连接器',
            children: (
              <Card variant="outlined">
                <Descriptions column={2} size="small" bordered>
                  <Descriptions.Item label="Hive">HMS Thrift Client（生产）</Descriptions.Item>
                  <Descriptions.Item label="MySQL">
                    SQLAlchemy + information_schema
                  </Descriptions.Item>
                  <Descriptions.Item label="Iceberg">REST Catalog</Descriptions.Item>
                  <Descriptions.Item label="dbt">manifest.json 解析</Descriptions.Item>
                  <Descriptions.Item label="调度">Airflow REST</Descriptions.Item>
                  <Descriptions.Item label="血缘">OpenLineage</Descriptions.Item>
                </Descriptions>
              </Card>
            ),
          },
        ]}
      />
    </div>
  );
}

export default Settings;

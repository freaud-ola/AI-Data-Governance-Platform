import { ApiOutlined, ExperimentOutlined, ThunderboltOutlined } from '@ant-design/icons';
import { Alert, Button, Card, Col, Input, Row, Space, Tag, Typography } from 'antd';
import { useState } from 'react';

import ModuleStatusBanner from '@/components/ModuleStatusBanner';
import PageHeader from '@/components/PageHeader';

const { TextArea } = Input;
const { Paragraph, Text } = Typography;

const SAMPLE_RESULT = `-- 上周（2026-04-21 ~ 2026-04-27）北京地区的 GMV
WITH base AS (
    SELECT
        order_id,
        order_amount,
        city,
        dt
    FROM prod.dw.dwd_order_detail
    WHERE dt BETWEEN '20260421' AND '20260427'
        AND city = '北京'
)
SELECT
    SUM(order_amount) AS gmv
FROM base
LIMIT 1000;`;

function NL2SQLPlayground() {
  const [question, setQuestion] = useState('上周北京地区的 GMV 是多少？');
  const [running, setRunning] = useState(false);
  const [sql, setSql] = useState<string>('');

  const onRun = () => {
    setRunning(true);
    setSql('');
    setTimeout(() => {
      setSql(SAMPLE_RESULT);
      setRunning(false);
    }, 800);
  };

  return (
    <div>
      <PageHeader
        title="NL2SQL Playground"
        subtitle="Schema Linking → Few-shot → Self-Correct → 安全护栏 — Phase 4 工业化"
        tags={[
          { color: 'orange', text: 'Phase 4' },
          { color: 'blue', text: '内测' },
        ]}
      />
      <ModuleStatusBanner stage="in-progress" arch="03-AI能力层设计 §工业级 NL2SQL" />

      <Row gutter={16}>
        <Col span={12}>
          <Card
            title={
              <>
                <ExperimentOutlined /> 自然语言提问
              </>
            }
            variant="outlined"
          >
            <TextArea
              rows={6}
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="例如：上周北京地区的 GMV 是多少？"
            />
            <Space style={{ marginTop: 12 }}>
              <Button
                type="primary"
                icon={<ThunderboltOutlined />}
                loading={running}
                onClick={onRun}
              >
                生成 SQL
              </Button>
              <Button icon={<ApiOutlined />} disabled>
                试运行（限制 LIMIT 1000）
              </Button>
            </Space>

            <div style={{ marginTop: 16 }}>
              <Text type="secondary">示例提问：</Text>
              <div style={{ marginTop: 8 }}>
                {[
                  '上周北京地区的 GMV 是多少？',
                  '近 7 天日活用户趋势',
                  '订单数 Top 10 的供应商',
                  '哪些表的最近一次更新超过 7 天？',
                ].map((q) => (
                  <Tag
                    key={q}
                    color="blue"
                    style={{ cursor: 'pointer', marginBottom: 6 }}
                    onClick={() => setQuestion(q)}
                  >
                    {q}
                  </Tag>
                ))}
              </div>
            </div>
          </Card>
        </Col>
        <Col span={12}>
          <Card title="生成 SQL（占位）" variant="outlined">
            {!sql && !running && (
              <Alert
                type="info"
                showIcon
                message="点击左侧『生成 SQL』演示。MVP 阶段返回占位脚本，Phase 4 接入工业级 NL2SQL pipeline。"
              />
            )}
            {running && <Alert type="info" message="正在调用 LLM…" showIcon />}
            {sql && (
              <pre
                style={{
                  background: '#0b1021',
                  color: '#f8f8f2',
                  padding: 16,
                  borderRadius: 8,
                  fontSize: 13,
                  overflow: 'auto',
                  margin: 0,
                }}
              >
                {sql}
              </pre>
            )}
            <Paragraph type="secondary" style={{ marginTop: 16, marginBottom: 0 }}>
              说明：MVP 阶段为静态示例，后续会接入 Schema Linking + Few-shot + Self-Correct +
              安全护栏（强制 LIMIT、只读账号、EXPLAIN 校验）。
            </Paragraph>
          </Card>
        </Col>
      </Row>
    </div>
  );
}

export default NL2SQLPlayground;

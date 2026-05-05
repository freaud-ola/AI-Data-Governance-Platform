import { Card, Col, Row, Statistic } from 'antd';

import ModuleStatusBanner from '@/components/ModuleStatusBanner';
import PageHeader from '@/components/PageHeader';

function Profiling() {
  return (
    <div>
      <PageHeader
        title="数据探查"
        subtitle="基础统计 / 分布 / 异常检测 / 采样 — 基于 Spark + Great Expectations"
        tags={[{ color: 'orange', text: 'Phase 2' }]}
      />
      <ModuleStatusBanner stage="in-progress" arch="02-数据质量与血缘 §探查引擎" />

      <Row gutter={16}>
        <Col span={6}>
          <Card variant="outlined">
            <Statistic title="待探查表" value={186} />
          </Card>
        </Col>
        <Col span={6}>
          <Card variant="outlined">
            <Statistic title="今日探查任务" value={42} />
          </Card>
        </Col>
        <Col span={6}>
          <Card variant="outlined">
            <Statistic title="探查覆盖率" value={62} suffix="%" />
          </Card>
        </Col>
        <Col span={6}>
          <Card variant="outlined">
            <Statistic title="发现异常分布" value={8} valueStyle={{ color: '#cf1322' }} />
          </Card>
        </Col>
      </Row>

      <Card style={{ marginTop: 16 }} title="探查任务（开发中）" variant="outlined">
        <div className="dg-placeholder">
          列表页占位：探查任务调度 + 结果可视化（直方图 / Top-N / Null 比例 / 唯一值）· Phase 2 完成
        </div>
      </Card>
    </div>
  );
}

export default Profiling;

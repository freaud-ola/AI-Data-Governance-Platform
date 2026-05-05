import { Card, Empty } from 'antd';

import ModuleStatusBanner from '@/components/ModuleStatusBanner';
import PageHeader from '@/components/PageHeader';

function Audit() {
  return (
    <div>
      <PageHeader
        title="审计日志"
        subtitle="API / SQL / LLM 调用全链路审计 — 6 个月热存储 + 5 年归档"
        tags={[{ color: 'red', text: 'P0' }]}
      />
      <ModuleStatusBanner stage="in-progress" arch="04-安全与合规 §审计" />

      <Card variant="outlined">
        <Empty description="审计 UI 占位 — 计划：操作日志 / 数据访问日志 / LLM 调用审计 + Loki 检索" />
      </Card>
    </div>
  );
}

export default Audit;

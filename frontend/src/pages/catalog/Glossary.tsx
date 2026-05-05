import { Card, Empty } from 'antd';

import ModuleStatusBanner from '@/components/ModuleStatusBanner';
import PageHeader from '@/components/PageHeader';

function Glossary() {
  return (
    <div>
      <PageHeader
        title="业务术语"
        subtitle="业务术语表 / 同义词 / 中英文映射 — Phase 2 上线"
        tags={[{ color: 'orange', text: 'Phase 2' }]}
      />
      <ModuleStatusBanner stage="in-progress" arch="01-元数据接入与建模 §业务语义层" />
      <Card variant="outlined">
        <Empty description="术语表 UI 占位 — 计划：树形分类 + 业务术语条目编辑 + AI 同义词推荐" />
      </Card>
    </div>
  );
}

export default Glossary;

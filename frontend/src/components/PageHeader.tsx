import { Space, Tag, Typography } from 'antd';
import type { ReactNode } from 'react';

const { Title, Paragraph } = Typography;

interface Props {
  title: string;
  subtitle?: string;
  tags?: { color?: string; text: string }[];
  extra?: ReactNode;
}

function PageHeader({ title, subtitle, tags, extra }: Props) {
  return (
    <div
      className="dg-page-header"
      style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between' }}
    >
      <div>
        <Space align="center" size={12}>
          <Title level={3} style={{ margin: 0 }}>
            {title}
          </Title>
          {tags?.map((t) => (
            <Tag key={t.text} color={t.color}>
              {t.text}
            </Tag>
          ))}
        </Space>
        {subtitle && (
          <Paragraph type="secondary" style={{ marginBottom: 0, marginTop: 4 }}>
            {subtitle}
          </Paragraph>
        )}
      </div>
      <div>{extra}</div>
    </div>
  );
}

export default PageHeader;

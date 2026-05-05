import { InfoCircleOutlined } from '@ant-design/icons';
import { Alert, Space } from 'antd';

type Stage = 'mvp-skeleton' | 'in-progress' | 'beta' | 'ga';

const STAGE_MAP: Record<Stage, { color: 'info' | 'warning' | 'success'; text: string }> = {
  'mvp-skeleton': { color: 'info', text: 'MVP 骨架版本，使用 Mock 数据展示，业务逻辑后续阶段接入' },
  'in-progress': { color: 'warning', text: '开发中：部分功能已接入真实底座，仍在迭代' },
  beta: { color: 'warning', text: '内测版本：可用但有已知问题，请勿用于生产' },
  ga: { color: 'success', text: '正式发布版本' },
};

interface Props {
  stage: Stage;
  arch?: string;
  arch_link?: string;
}

function ModuleStatusBanner({ stage, arch, arch_link }: Props) {
  const cfg = STAGE_MAP[stage];
  return (
    <Alert
      type={cfg.color}
      showIcon
      icon={<InfoCircleOutlined />}
      style={{ marginBottom: 16 }}
      message={
        <Space size={8} wrap>
          <span>{cfg.text}</span>
          {arch && (
            <span style={{ color: 'rgba(0,0,0,0.55)' }}>
              · 架构参考：
              {arch_link ? (
                <a href={arch_link} target="_blank" rel="noreferrer">
                  {arch}
                </a>
              ) : (
                arch
              )}
            </span>
          )}
        </Space>
      }
    />
  );
}

export default ModuleStatusBanner;

import { LogoutOutlined, UserOutlined } from '@ant-design/icons';
import { ProLayout } from '@ant-design/pro-components';
import { Dropdown, Space, Tag } from 'antd';
import { Outlet, useLocation, useNavigate } from 'react-router-dom';

import ErrorBoundary from '@/components/ErrorBoundary';
import { MENU_GROUPS } from '@/routes/routes';

const proLayoutRoutes = {
  path: '/',
  routes: MENU_GROUPS.map((g) => ({
    path: `/_group/${g.key}`,
    name: g.name,
    icon: g.icon,
    routes: g.children.map((c) => ({
      path: c.path,
      name: c.name,
      icon: c.icon,
    })),
  })),
};

function MainLayout() {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <ProLayout
      title="AI 数据治理平台"
      logo={<img src="/favicon.svg" alt="logo" style={{ height: 32 }} />}
      layout="mix"
      contentWidth="Fluid"
      fixedHeader
      fixSiderbar
      location={{ pathname: location.pathname }}
      route={proLayoutRoutes}
      siderWidth={232}
      menu={{ defaultOpenAll: true }}
      menuItemRender={(item, dom) => (
        <a
          onClick={(e) => {
            e.preventDefault();
            if (item.path && !item.path.startsWith('/_group')) {
              navigate(item.path);
            }
          }}
        >
          {dom}
        </a>
      )}
      avatarProps={{
        src: undefined,
        size: 'small',
        title: 'admin',
        icon: <UserOutlined />,
        render: (_props, dom) => (
          <Dropdown
            menu={{
              items: [
                { key: 'profile', icon: <UserOutlined />, label: '个人中心' },
                { type: 'divider' },
                { key: 'logout', icon: <LogoutOutlined />, label: '退出登录' },
              ],
            }}
          >
            {dom}
          </Dropdown>
        ),
      }}
      actionsRender={() => [
        <Space key="tenant" size={6} style={{ color: 'rgba(0,0,0,0.65)' }}>
          <Tag color="blue">租户：default</Tag>
          <Tag color="purple">环境：dev</Tag>
        </Space>,
      ]}
      footerRender={() => (
        <div style={{ textAlign: 'center', padding: 12, color: 'rgba(0,0,0,0.45)' }}>
          AI Data Governance Platform · MVP v0.1 · 基于 v2 架构搭建
        </div>
      )}
    >
      <div style={{ padding: 16, minHeight: 'calc(100vh - 96px)' }}>
        <ErrorBoundary resetKey={location.pathname}>
          <Outlet />
        </ErrorBoundary>
      </div>
    </ProLayout>
  );
}

export default MainLayout;

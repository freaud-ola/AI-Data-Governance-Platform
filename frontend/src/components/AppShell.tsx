import { App as AntdApp } from 'antd';
import { useEffect, type ReactNode } from 'react';

import { setMessageApi, setNotificationApi } from '@/utils/feedback';

/**
 * 通过 `App.useApp()` 把 message / notification 实例注入到全局桥（feedback.ts），
 * 这样非 React 上下文（axios / Query 全局回调等）也能弹 toast，且能继承当前主题。
 */
function FeedbackBridge() {
  const { message, notification } = AntdApp.useApp();
  useEffect(() => {
    setMessageApi(message);
    setNotificationApi(notification);
    return () => {
      setMessageApi(null);
      setNotificationApi(null);
    };
  }, [message, notification]);
  return null;
}

export default function AppShell({ children }: { children: ReactNode }) {
  return (
    <AntdApp message={{ maxCount: 3 }} notification={{ placement: 'topRight', maxCount: 3 }}>
      <FeedbackBridge />
      {children}
    </AntdApp>
  );
}

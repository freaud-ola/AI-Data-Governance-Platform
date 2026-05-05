/**
 * 全局 message / notification 桥。
 *
 * AntD v5 推荐通过 `App.useApp()` 使用 message / notification（这样能继承 ConfigProvider
 * 的主题与 locale）。我们在 `<App>` Provider 内通过一个挂载组件把实例注入到这里，
 * 再由非 React 模块（如 axios 拦截器、TanStack Query 全局回调）调用。
 */

import type { MessageInstance } from 'antd/es/message/interface';
import type { NotificationInstance } from 'antd/es/notification/interface';

let messageApi: MessageInstance | null = null;
let notificationApi: NotificationInstance | null = null;

export function setMessageApi(api: MessageInstance | null) {
  messageApi = api;
}

export function setNotificationApi(api: NotificationInstance | null) {
  notificationApi = api;
}

type Severity = 'success' | 'info' | 'warning' | 'error';

function fallback(severity: Severity, content: string) {
  // App Provider 还没挂载时（极少发生）至少不丢失信息
  const tag = `[${severity.toUpperCase()}]`;
  if (severity === 'error' || severity === 'warning') {
    console.error(tag, content);
  } else {
    console.warn(tag, content);
  }
}

export const toast = {
  success(content: string) {
    if (messageApi) messageApi.success(content);
    else fallback('success', content);
  },
  info(content: string) {
    if (messageApi) messageApi.info(content);
    else fallback('info', content);
  },
  warning(content: string) {
    if (messageApi) messageApi.warning(content);
    else fallback('warning', content);
  },
  error(content: string) {
    if (messageApi) messageApi.error(content);
    else fallback('error', content);
  },
};

export const notify = {
  success(message: string, description?: string) {
    notificationApi?.success({ message, description });
  },
  info(message: string, description?: string) {
    notificationApi?.info({ message, description });
  },
  warning(message: string, description?: string) {
    notificationApi?.warning({ message, description });
  },
  error(message: string, description?: string) {
    notificationApi?.error({ message, description });
  },
};

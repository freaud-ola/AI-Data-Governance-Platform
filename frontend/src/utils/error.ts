import type { AxiosError } from 'axios';

import type { ApiResponse } from '@/api/client';

/**
 * 从任意错误对象中抽出对用户友好的消息文案。
 *
 * 优先级：
 *   1. 后端 ApiResponse.message（业务错误）
 *   2. HTTP statusText
 *   3. 已知 axios code / message（超时 / 断网）
 *   4. error.message
 *   5. 兜底 "未知错误"
 */
export function getErrorMessage(err: unknown): string {
  if (typeof err === 'string') return err;

  if (err && typeof err === 'object') {
    const ax = err as AxiosError<ApiResponse<unknown>>;

    if (ax.isAxiosError) {
      const data = ax.response?.data;
      if (data && typeof data === 'object' && 'message' in data && data.message) {
        return String(data.message);
      }
      if (ax.response?.status) {
        const text = ax.response.statusText || '请求失败';
        return `${ax.response.status} ${text}`;
      }
      if (ax.code === 'ECONNABORTED') return '请求超时，请稍后重试';
      if (ax.message === 'Network Error') return '网络异常，请检查后端服务是否启动';
      if (ax.message) return ax.message;
    }

    const candidate = (err as { message?: unknown }).message;
    if (typeof candidate === 'string' && candidate.trim()) return candidate;
  }

  return '未知错误';
}

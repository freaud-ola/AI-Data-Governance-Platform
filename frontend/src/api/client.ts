import axios, { type AxiosInstance } from 'axios';

const baseURL = '/api/v1';

export const apiClient: AxiosInstance = axios.create({
  baseURL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
    'X-Tenant-Id': 'default',
  },
});

apiClient.interceptors.response.use(
  (resp) => {
    // 后端约定的统一包装：{ success, code, message, data }
    // 业务失败（HTTP 200 + success=false）也应作为错误抛出，统一走 onError。
    const body = resp.data;
    if (body && typeof body === 'object' && 'success' in body && body.success === false) {
      const err = new Error(typeof body.message === 'string' ? body.message : '业务错误');
      // 把原始响应挂上去，方便调用方拿 code 做差异化处理
      (err as Error & { response?: typeof resp }).response = resp;
      return Promise.reject(err);
    }
    return resp;
  },
  (error) => Promise.reject(error),
);

export interface ApiResponse<T> {
  success: boolean;
  code: number;
  message: string;
  data: T;
}

export interface PageMeta {
  page: number;
  page_size: number;
  total: number;
}

export interface PageData<T> {
  items: T[];
  meta: PageMeta;
}

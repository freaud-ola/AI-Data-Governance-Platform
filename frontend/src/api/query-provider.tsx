import { MutationCache, QueryCache, QueryClient, QueryClientProvider } from '@tanstack/react-query';
import type { ReactNode } from 'react';

import { getErrorMessage } from '@/utils/error';
import { toast } from '@/utils/feedback';

const client = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 30_000,
    },
    mutations: {
      retry: 0,
    },
  },
  queryCache: new QueryCache({
    onError: (err, query) => {
      // 单个 query 显式声明 meta.silent 时，不自动 toast（用于轮询 / 静默刷新）
      if (query.meta?.silent) return;
      toast.error(getErrorMessage(err));
    },
  }),
  mutationCache: new MutationCache({
    onError: (err, _vars, _ctx, mutation) => {
      if (mutation.meta?.silent) return;
      toast.error(getErrorMessage(err));
    },
  }),
});

export function QueryProvider({ children }: { children: ReactNode }) {
  return <QueryClientProvider client={client}>{children}</QueryClientProvider>;
}

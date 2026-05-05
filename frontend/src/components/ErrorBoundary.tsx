import { Button, Result, Typography } from 'antd';
import { Component, type ErrorInfo, type ReactNode } from 'react';

interface Props {
  children: ReactNode;
  /** 当前路由 path，路由切换时自动重置错误状态 */
  resetKey?: string;
}

interface State {
  hasError: boolean;
  error?: Error;
}

const { Paragraph } = Typography;

/**
 * 顶层兜底错误边界。捕获子树未处理的渲染期异常，渲染降级 UI 而不是白屏。
 *
 * 注意：React 的错误边界不会捕获事件回调、setTimeout 与 Promise 中的异常；
 * 这些走 axios / TanStack Query 的全局错误回调（参见 query-provider.tsx）。
 */
export default class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error('[ErrorBoundary]', error, info);
  }

  componentDidUpdate(prev: Props) {
    if (this.state.hasError && prev.resetKey !== this.props.resetKey) {
      this.setState({ hasError: false, error: undefined });
    }
  }

  private handleReload = () => {
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <Result
          status="error"
          title="页面出错了"
          subTitle="抱歉，渲染过程中发生了未预期的异常。请尝试刷新页面，如反复出现请联系平台管理员。"
          extra={[
            <Button key="reload" type="primary" onClick={this.handleReload}>
              刷新重试
            </Button>,
          ]}
        >
          {this.state.error && (
            <Paragraph type="secondary" style={{ whiteSpace: 'pre-wrap', textAlign: 'left' }}>
              {this.state.error.message}
            </Paragraph>
          )}
        </Result>
      );
    }
    return this.props.children;
  }
}

'use client';

import { ChatProvider } from '@/components/ChatContext';

export function Providers({ children }: { children: React.ReactNode }) {
  return <ChatProvider>{children}</ChatProvider>;
}

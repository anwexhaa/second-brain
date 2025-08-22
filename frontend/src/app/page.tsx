'use client';

import Sidebar from '@/components/Sidebar';
import KnowledgeOrb from '@/components/KnowledgeOrb';
import ChatWindow from '@/components/ChatWindow';
import ChatInput from '@/components/ChatInput';
import { ChatProvider } from '@/components/ChatContext';
import styles from './page.module.css';

export default function HomePage() {
  return (
    <ChatProvider>
      <div style={{ display: 'flex' }}>
        <Sidebar />
        <main className={styles.container} style={{ flexGrow: 1 }}>
          <div className={styles.orbWrapper}>
            <KnowledgeOrb />
          </div>
          <ChatWindow />
          <ChatInput />
        </main>
      </div>
    </ChatProvider>
  );
}

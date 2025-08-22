'use client';
import Sidebar from '@/components/Sidebar';
import KnowledgeOrb from '@/components/KnowledgeOrb';
import ChatWindow from '@/components/ChatWindow';
import ChatInput from '@/components/ChatInput';
import styles from './upload.module.css';

export default function UploadPage() {
  return (
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
  );
}

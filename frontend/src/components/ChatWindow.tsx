'use client';

import { useEffect, useRef } from 'react';
import { useChat } from './ChatContext';
import styles from './ChatWindow.module.css';

export default function ChatWindow() {
  const { messages, isTyping } = useChat();
  const endOfMessagesRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  return (
    <div className={styles.chatContainer}>
      {messages.map((msg, idx) => (
        <div
          key={idx}
          className={`${styles.message} ${
            msg.sender === 'user' ? styles.userMessage : styles.aiMessage
          }`}
        >
          <strong>{msg.sender === 'user' ? 'You' : 'AI'}:</strong> {msg.text}
        </div>
      ))}

      {isTyping && (
        <div className={`${styles.message} ${styles.aiMessage}`}>
          <strong>AI:</strong> ...
        </div>
      )}

      <div ref={endOfMessagesRef} />
    </div>
  );
}

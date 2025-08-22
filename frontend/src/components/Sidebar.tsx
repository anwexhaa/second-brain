'use client';

import { useState } from 'react';
import { useChat } from './ChatContext';
import styles from './Sidebar.module.css';
import { Pencil, Check } from 'lucide-react';

export default function Sidebar() {
  const {
    chats,
    currentChatId,
    switchChat,
    createNewChat,
    hasEmptyChat,
    renameChat,
  } = useChat();

  const [editingId, setEditingId] = useState<string | null>(null);
  const [newTitle, setNewTitle] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  const handleRename = (id: string) => {
    if (newTitle.trim()) {
      renameChat(id, newTitle.trim());
    }
    setEditingId(null);
    setNewTitle('');
  };

  const filteredChats = chats.filter((chat) => {
    const title = chat.title
      ? chat.title
      : chat.messages.length > 0
        ? chat.messages[0].text
        : 'New Chat';
    return title.toLowerCase().includes(searchQuery.toLowerCase());
  });

  return (
    <div className={styles.sidebar}>
      <button
        className={styles.newChat}
        onClick={createNewChat}
        disabled={hasEmptyChat}
      >
        + New Chat
      </button>

      <input
        type="text"
        className={styles.searchInput}
        placeholder="Search Chats"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
      />

      <div className={styles.chatList}>
        {filteredChats.map((chat) => (
          <div
            key={chat.id}
            className={`${styles.chatItem} ${chat.id === currentChatId ? styles.activeChat : ''}`}
          >
            {editingId === chat.id ? (
              <div className={styles.renameWrapper}>
                <input
                  className={styles.renameInput}
                  value={newTitle}
                  onChange={(e) => setNewTitle(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleRename(chat.id)}
                  autoFocus
                />
                <button onClick={() => handleRename(chat.id)} className={styles.renameIcon}>
                  <Check size={14} />
                </button>
              </div>
            ) : (
              <div className={styles.chatRow}>
                <div onClick={() => switchChat(chat.id)} className={styles.chatTitle}>
                  {chat.title
                    ? chat.title
                    : chat.messages.length > 0
                      ? `${chat.messages[0].text.slice(0, 20)}...`
                      : 'New Chat'}
                </div>
                <button
                  onClick={() => {
                    setEditingId(chat.id);
                    setNewTitle(
                      chat.title ||
                      (chat.messages.length > 0
                        ? `${chat.messages[0].text.slice(0, 20)}`
                        : 'New Chat')
                    );
                  }}
                  className={styles.renameIcon}
                >
                  <Pencil size={14} />
                </button>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

'use client';

import { useState, useRef } from 'react';
import styles from '@/app/page.module.css';
import { useChat } from './ChatContext';
import { FilePlus2, ArrowUpFromLine, Loader2 } from "lucide-react";
import { auth } from '@/lib/firebase';

export default function ChatInput() {
  const { addMessage, setIsTyping, isTyping } = useChat();
  const [message, setMessage] = useState('');
  const [fileName, setFileName] = useState('');
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (!selectedFile || uploading) return;

    setUploading(true);
    setFileName(selectedFile.name);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/upload/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) throw new Error(`Upload failed: ${await res.text()}`);

      addMessage({ sender: 'bot', text: `📄 Uploaded: ${selectedFile.name}` });
    } catch (err) {
      console.error('Upload error:', err);
      addMessage({ sender: 'bot', text: '⚠️ File upload failed.' });
      setFileName('');
    } finally {
      setUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handleSubmit = async () => {
    const trimmed = message.trim();
    if (!trimmed) return;

    setMessage('');
    addMessage({ sender: 'user', text: trimmed });
    setIsTyping(true);

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: trimmed, namespace: 'default' }),
      });

      if (!res.ok) throw new Error(`AI response failed: ${await res.text()}`);

      const data = await res.json();
      const aiReply = Array.isArray(data.answer)
        ? data.answer.join('\n')
        : data.answer || 'No response from AI.';

      addMessage({ sender: 'bot', text: aiReply });
    } catch (err) {
      console.error('Fetch error:', err);
      addMessage({ sender: 'bot', text: '⚠️ Error fetching AI response.' });
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className={styles.bottomBar}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <label className={styles.iconButton}>
          <FilePlus2 size={20} />
          <input type="file" hidden ref={fileInputRef} onChange={handleFileChange} />
        </label>

        {(uploading || isTyping) && (
          <div className={styles.spinner}>
            <Loader2 size={20} className="animate-spin" />
          </div>
        )}
      </div>

      <input
        type="text"
        placeholder="Ask a question..."
        className={styles.input}
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}
      />

      <button className={styles.iconButton} onClick={handleSubmit}>
        <ArrowUpFromLine size={20} />
      </button>
    </div>
  );
}

'use client';
import ChatWindow from '@/components/ChatWindow';
import ChatInput from '@/components/ChatInput';

export default function ChatPage() {
  return (
    <div className="flex flex-col h-screen">
      <div className="flex-1 overflow-hidden">
        <ChatWindow />
      </div>
      <ChatInput />
    </div>
  );
}
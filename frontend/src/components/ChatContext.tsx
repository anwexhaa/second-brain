'use client';

import {
  createContext,
  useContext,
  useState,
  ReactNode,
  useMemo,
  useEffect,
} from 'react';
import {
  collection,
  query,
  orderBy,
  onSnapshot,
  addDoc,
  serverTimestamp,
} from 'firebase/firestore';
import { auth, db } from '@/lib/firebase';

export interface Message {
  sender: 'user' | 'bot';
  text: string;
}

export interface ChatSession {
  id: string;
  title?: string;
  messages: Message[];
}

interface ChatContextType {
  chats: ChatSession[];
  currentChatId: string;
  messages: Message[];
  addMessage: (msg: Message) => void;
  createNewChat: () => void;
  switchChat: (id: string) => void;
  renameChat: (id: string, newTitle: string) => void;
  hasEmptyChat: boolean;
  isTyping: boolean;
  setIsTyping: (val: boolean) => void;
}

const ChatContext = createContext<ChatContextType>({
  chats: [],
  currentChatId: '',
  messages: [],
  addMessage: () => {},
  createNewChat: () => {},
  switchChat: () => {},
  renameChat: () => {},
  hasEmptyChat: false,
  isTyping: false,
  setIsTyping: () => {},
});

export const ChatProvider = ({ children }: { children: ReactNode }) => {
  const [chats, setChats] = useState<ChatSession[]>([
    { id: 'chat-1', messages: [] },
  ]);
  const [currentChatId, setCurrentChatId] = useState('chat-1');
  const [isTyping, setIsTyping] = useState(false);

  const currentChat = chats.find((chat) => chat.id === currentChatId);
  const messages = currentChat ? currentChat.messages : [];

  const hasEmptyChat = useMemo(
    () => chats.some((chat) => chat.messages.length === 0),
    [chats],
  );

  // 🔥 Firestore listener for current chat
  useEffect(() => {
    if (!auth.currentUser) return;

    const userId = auth.currentUser.uid;
    const messagesRef = collection(
      db,
      'users',
      userId,
      'chats',
      currentChatId,
      'messages',
    );
    const q = query(messagesRef, orderBy('createdAt', 'asc'));

    const unsubscribe = onSnapshot(
      q,
      (snapshot) => {
        const firestoreMessages = snapshot.docs.map((doc) => {
          const data = doc.data();
          return {
            sender: data.sender as 'user' | 'bot',
            text: data.text as string,
          };
        });

        setChats((prevChats) =>
          prevChats.map((chat) =>
            chat.id === currentChatId
              ? { ...chat, messages: firestoreMessages }
              : chat,
          ),
        );
      },
      (error) => {
        console.error('Firestore listener error:', error);
      },
    );

    return () => unsubscribe();
  }, [currentChatId]);

  // ✅ Optimistic update + Firestore write
  const addMessage = async (msg: Message) => {
    // 1. Update local state immediately
    setChats((prevChats) =>
      prevChats.map((chat) =>
        chat.id === currentChatId
          ? { ...chat, messages: [...chat.messages, msg] }
          : chat,
      ),
    );

    // 2. Write to Firestore
    if (!auth.currentUser) {
      console.warn('User not logged in, cannot save message');
      return;
    }

    const userId = auth.currentUser.uid;
    const messagesRef = collection(
      db,
      'users',
      userId,
      'chats',
      currentChatId,
      'messages',
    );

    try {
      await addDoc(messagesRef, {
        text: msg.text,
        sender: msg.sender,
        createdAt: serverTimestamp(),
      });
    } catch (error) {
      console.error('Error adding message to Firestore:', error);
    }
  };

  const createNewChat = () => {
    if (hasEmptyChat) {
      const emptyChat = chats.find((chat) => chat.messages.length === 0);
      if (emptyChat) {
        setCurrentChatId(emptyChat.id);
      }
      return;
    }

    const newId = `chat-${Date.now()}`;
    const newChat: ChatSession = { id: newId, messages: [] };
    setChats((prev) => [...prev, newChat]);
    setCurrentChatId(newId);
  };

  const switchChat = (id: string) => {
    setCurrentChatId(id);
  };

  const renameChat = (id: string, newTitle: string) => {
    setChats((prevChats) =>
      prevChats.map((chat) =>
        chat.id === id ? { ...chat, title: newTitle } : chat,
      ),
    );
  };

  return (
    <ChatContext.Provider
      value={{
        chats,
        currentChatId,
        messages,
        addMessage,
        createNewChat,
        switchChat,
        renameChat,
        hasEmptyChat,
        isTyping,
        setIsTyping,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};

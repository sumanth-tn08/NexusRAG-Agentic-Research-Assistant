import React, { useState, useEffect, useCallback } from 'react';
import Sidebar from './Sidebar';
import ChatWindow from './ChatWindow';
import { checkHealth, sendChatMessage, deleteSession, deleteDocument } from '../services/api';
import type { UploadedDocument, ChatMessage as ChatMessageType } from '../types';

const SESSION_STORAGE_KEY = 'nexusrag_session_id';

const getInitialSessionId = (): string => {
  const existing = localStorage.getItem(SESSION_STORAGE_KEY);
  if (existing) return existing;
  const newId = crypto.randomUUID();
  localStorage.setItem(SESSION_STORAGE_KEY, newId);
  return newId;
};

export const Layout: React.FC = () => {
  const [sessionId, setSessionId] = useState<string>(getInitialSessionId);
  const [documents, setDocuments] = useState<UploadedDocument[]>([]);
  const [selectedDocumentIds, setSelectedDocumentIds] = useState<string[]>([]);
  const [messages, setMessages] = useState<ChatMessageType[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState<boolean>(false);

  // Health check on mount and interval
  useEffect(() => {
    let isMounted = true;

    const verifyBackend = async () => {
      const healthy = await checkHealth();
      if (isMounted) {
        setIsConnected(healthy);
      }
    };

    verifyBackend();
    const interval = setInterval(verifyBackend, 10000);

    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  // Debug logging for state consistency
  useEffect(() => {
    console.log('CURRENT DOCUMENTS:', documents);
  }, [documents]);

  useEffect(() => {
    console.log('SELECTED DOCUMENT IDS:', selectedDocumentIds);
  }, [selectedDocumentIds]);

  const handleUploadSuccess = useCallback((newDoc: UploadedDocument) => {
    setDocuments((prev) => [newDoc, ...prev.filter((d) => d.document_id !== newDoc.document_id)]);
    setSelectedDocumentIds((prev) =>
      prev.includes(newDoc.document_id) ? prev : [...prev, newDoc.document_id]
    );
  }, []);

  // Toggle document selection
  const handleToggleSelect = (documentId: string) => {
    setSelectedDocumentIds((prev) =>
      prev.includes(documentId) ? prev.filter((id) => id !== documentId) : [...prev, documentId]
    );
  };

  // Delete document with backend call
  const handleDeleteDocument = async (documentId: string) => {
    try {
      await deleteDocument(documentId);
      setDocuments((prev) => prev.filter((doc) => doc.document_id !== documentId));
      setSelectedDocumentIds((prev) => prev.filter((id) => id !== documentId));
    } catch (err: any) {
      console.error('Failed to delete document:', err);
      const detail = err.response?.data?.detail || err.message || 'Deletion failed.';
      const errorMessage: ChatMessageType = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: `Failed to delete document: ${detail}`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, errorMessage]);
    }
  };

  const handleSendMessage = useCallback(
    async (content: string) => {
      // Ensure at least one document selected
      if (selectedDocumentIds.length === 0) {
        const warningMessage: ChatMessageType = {
          id: crypto.randomUUID(),
          role: 'assistant',
          content: 'Select at least one document to search.',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        };
        setMessages((prev) => [...prev, warningMessage]);
        return;
      }

      const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

      const userMessage: ChatMessageType = {
        id: crypto.randomUUID(),
        role: 'user',
        content,
        timestamp: now,
      };

      setMessages((prev) => [...prev, userMessage]);
      setIsLoading(true);

      try {
        const response = await sendChatMessage(content, sessionId, selectedDocumentIds);
        const assistantMessage: ChatMessageType = {
          id: crypto.randomUUID(),
          role: 'assistant',
          content: response.answer,
          sources: response.sources || [],
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        };
        setMessages((prev) => [...prev, assistantMessage]);
      } catch (error: any) {
        console.error('Chat error:', error);
        const detail =
          error.response?.data?.detail ||
          error.message ||
          'Something went wrong while generating the answer. Please check the backend connection and try again.';
        const errorMessage: ChatMessageType = {
          id: crypto.randomUUID(),
          role: 'assistant',
          content: `Error: ${detail}`,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        };
        setMessages((prev) => [...prev, errorMessage]);
      } finally {
        setIsLoading(false);
      }
    },
    [sessionId, selectedDocumentIds]
  );

  const handleNewChat = useCallback(() => {
    const newSessionId = crypto.randomUUID();
    localStorage.setItem(SESSION_STORAGE_KEY, newSessionId);
    setSessionId(newSessionId);
    setMessages([]);
    // keep documents and selection unchanged
  }, []);

  const handleClearChat = useCallback(async () => {
    try {
      await deleteSession(sessionId);
    } catch (err) {
      console.error('Failed to clear session on backend:', err);
    } finally {
      setMessages([]);
    }
  }, [sessionId]);

  // Documents currently selected for searching (used for UI indicator)
  const selectedDocuments = documents.filter((doc) => selectedDocumentIds.includes(doc.document_id));

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-[#0b0f19]">
      <Sidebar
        documents={documents}
        onUploadSuccess={handleUploadSuccess}
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
        isBackendConnected={isConnected}
        selectedIds={selectedDocumentIds}
        onToggleSelect={handleToggleSelect}
        onDelete={handleDeleteDocument}
      />

      <ChatWindow
        messages={messages}
        isLoading={isLoading}
        isConnected={isConnected}
        onSendMessage={handleSendMessage}
        onNewChat={handleNewChat}
        onClearChat={handleClearChat}
        onToggleSidebar={() => setIsSidebarOpen((prev) => !prev)}
        documentCount={documents.length}
        selectedDocuments={selectedDocuments}
      />
    </div>
  );
};

export default Layout;

import React, { useEffect, useRef } from 'react';
import type { UploadedDocument, ConnectionStatus, ChatMessage as ChatMessageType } from '../types';
import { Menu, PlusCircle, Trash2, Bot, Sparkles, ShieldCheck, AlertCircle } from 'lucide-react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import LoadingIndicator from './LoadingIndicator';

interface ChatWindowProps {
  messages: ChatMessageType[];
  isLoading: boolean;
  isConnected?: boolean;
  connectionStatus: ConnectionStatus;
  onRetryConnection?: () => void;
  onSendMessage: (content: string) => void;
  onNewChat: () => void;
  onClearChat: () => void;
  onToggleSidebar: () => void;
  documentCount: number;
  selectedDocuments?: UploadedDocument[];
}

export const ChatWindow: React.FC<ChatWindowProps> = ({
  messages,
  isLoading,
  isConnected,
  connectionStatus,
  onRetryConnection,
  onSendMessage,
  onNewChat,
  onClearChat,
  onToggleSidebar,
  documentCount,
  selectedDocuments,
}) => {
  const scrollEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll on new messages or loading state
  useEffect(() => {
    scrollEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const isActuallyConnected = connectionStatus === 'connected' || (isConnected && connectionStatus !== 'disconnected');
  const isConnecting = connectionStatus === 'waking' || connectionStatus === 'checking';

  return (
    <main className="flex-1 flex flex-col h-full bg-[#0b0f19] text-slate-100 overflow-hidden relative">
      {/* Top Navbar */}
      <header className="h-16 border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md px-4 md:px-6 flex items-center justify-between flex-shrink-0 z-10">
        <div className="flex items-center space-x-3">
          <button
            onClick={onToggleSidebar}
            className="md:hidden p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            aria-label="Toggle sidebar"
          >
            <Menu className="w-5 h-5" />
          </button>

          <div>
            <div className="flex items-center space-x-2">
              <h2 className="text-base font-bold text-white tracking-tight">NexusRAG</h2>
              <span className="hidden sm:inline-block text-xs text-slate-400 font-medium">
                — Agentic Research Assistant
              </span>
            </div>
            <div className="flex items-center space-x-2 mt-0.5">
              <div className="flex items-center space-x-1.5">
                <span
                  className={`w-2 h-2 rounded-full ${
                    isActuallyConnected
                      ? 'bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.7)] animate-pulse'
                      : isConnecting
                      ? 'bg-amber-400 shadow-[0_0_8px_rgba(251,191,36,0.6)] animate-pulse'
                      : 'bg-red-500'
                  }`}
                />
                <span
                  className={`text-[11px] font-medium ${
                    isActuallyConnected
                      ? 'text-emerald-400'
                      : isConnecting
                      ? 'text-amber-400'
                      : 'text-red-400'
                  }`}
                >
                  {isActuallyConnected
                    ? 'Connected'
                    : isConnecting
                    ? 'Connecting (Waking up...)'
                    : 'Backend Disconnected'}
                </span>
              </div>
              <span className="text-slate-600 text-[10px]">•</span>
              <span className="text-[11px] text-slate-400 font-medium">
                {documentCount} {documentCount === 1 ? 'document' : 'documents'} loaded
              </span>
              {selectedDocuments && selectedDocuments.length > 0 && (
                <span
                  className="ml-2 text-[11px] text-indigo-400 font-medium truncate max-w-[200px] sm:max-w-xs md:max-w-md"
                  title={selectedDocuments.map((doc) => doc.filename).join(', ')}
                >
                  Searching: {selectedDocuments.map((doc) => doc.filename).join(', ')}
                </span>
              )}
            </div>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center space-x-2">
          <button
            onClick={onNewChat}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-800 hover:border-slate-700 transition-all cursor-pointer shadow-xs active:scale-[0.98]"
            title="Start a fresh chat with a new session ID"
          >
            <PlusCircle className="w-3.5 h-3.5 text-indigo-400" />
            <span className="hidden sm:inline">New Chat</span>
          </button>

          <button
            onClick={onClearChat}
            disabled={messages.length === 0}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-red-400 border border-slate-800 hover:border-red-900/40 disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:text-slate-300 transition-all cursor-pointer shadow-xs active:scale-[0.98]"
            title="Clear conversation history from backend"
          >
            <Trash2 className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Clear Chat</span>
          </button>
        </div>
      </header>

      {/* Backend Waking Banner */}
      {isConnecting && (
        <div className="bg-amber-950/60 border-b border-amber-900/50 px-4 py-2 flex items-center justify-center space-x-2 text-xs text-amber-200 animate-fade-in">
          <div className="w-3.5 h-3.5 border-2 border-amber-400/40 border-t-amber-400 rounded-full animate-spin flex-shrink-0" />
          <span>Connecting to backend (if waking from free-tier sleep, this may take ~30-50s)...</span>
        </div>
      )}

      {/* Backend Offline Banner */}
      {connectionStatus === 'disconnected' && (
        <div className="bg-red-950/60 border-b border-red-900/50 px-4 py-2 flex items-center justify-center space-x-2 text-xs text-red-200">
          <AlertCircle className="w-4 h-4 text-red-400 flex-shrink-0" />
          <span>Unable to connect to NexusRAG backend. Please ensure the backend server is running.</span>
          {onRetryConnection && (
            <button
              onClick={onRetryConnection}
              className="ml-2 underline text-red-300 hover:text-white cursor-pointer font-medium"
            >
              Retry
            </button>
          )}
        </div>
      )}

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto px-4 sm:px-6 md:px-8 py-6">
        <div className="max-w-4xl mx-auto w-full">
          {messages.length === 0 ? (
            /* Empty state welcome card */
            <div className="py-12 px-4 flex flex-col items-center text-center max-w-xl mx-auto animate-fade-in">
              <div className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-violet-500 flex items-center justify-center text-white shadow-xl shadow-indigo-600/25 mb-4">
                <Bot className="w-7 h-7" />
              </div>
              <h2 className="text-2xl font-bold text-white tracking-tight">
                Welcome to NexusRAG
              </h2>
              <p className="text-sm text-slate-400 mt-2 leading-relaxed">
                Your agentic document research assistant powered by LangGraph, Qdrant vector search, and conversational memory.
              </p>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full mt-8 text-left">
                <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800/80">
                  <div className="flex items-center space-x-2 text-indigo-400 mb-1">
                    <Sparkles className="w-4 h-4" />
                    <span className="text-xs font-semibold uppercase tracking-wider">Document Grounding</span>
                  </div>
                  <p className="text-xs text-slate-300">
                    Upload course notes, textbook chapters, or research papers via the sidebar.
                  </p>
                </div>

                <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800/80">
                  <div className="flex items-center space-x-2 text-violet-400 mb-1">
                    <ShieldCheck className="w-4 h-4" />
                    <span className="text-xs font-semibold uppercase tracking-wider">Citations & Tools</span>
                  </div>
                  <p className="text-xs text-slate-300">
                    NexusRAG retrieves precise chunk citations with page numbers and supports calculation tools.
                  </p>
                </div>
              </div>

              {documentCount === 0 && (
                <div className="mt-8 p-3 rounded-xl bg-indigo-950/30 border border-indigo-800/40 text-xs text-indigo-300">
                  💡 Start by uploading a PDF document in the left sidebar, or ask a question directly!
                </div>
              )}
            </div>
          ) : (
            <>
              {messages.map((msg) => (
                <ChatMessage key={msg.id} message={msg} />
              ))}
              {isLoading && <LoadingIndicator message="NexusRAG is thinking..." />}
            </>
          )}
          <div ref={scrollEndRef} />
        </div>
      </div>

      {/* Input Section */}
      <footer className="p-4 border-t border-slate-800/80 bg-slate-950/80 backdrop-blur-md flex-shrink-0">
        <ChatInput
          onSendMessage={onSendMessage}
          disabled={isLoading}
          connectionStatus={connectionStatus}
          isBackendConnected={isActuallyConnected}
        />
      </footer>
    </main>
  );
};

export default ChatWindow;

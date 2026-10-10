import React, { useState, useRef, useEffect } from 'react';
import { Send, CornerDownLeft } from 'lucide-react';
import type { ConnectionStatus } from '../types';

interface ChatInputProps {
  onSendMessage: (content: string) => void;
  disabled?: boolean;
  connectionStatus?: ConnectionStatus;
  isBackendConnected?: boolean;
}

export const ChatInput: React.FC<ChatInputProps> = ({
  onSendMessage,
  disabled = false,
  connectionStatus,
  isBackendConnected = true,
}) => {
  const [input, setInput] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea height as content changes
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 180)}px`;
    }
  }, [input]);

  const handleSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed || disabled) return;

    onSendMessage(trimmed);
    setInput('');

    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const isOffline = connectionStatus === 'disconnected' || (!connectionStatus && isBackendConnected === false);
  const isConnecting = connectionStatus === 'waking' || connectionStatus === 'checking';

  return (
    <div className="relative w-full max-w-4xl mx-auto">
      <form onSubmit={handleSubmit} className="relative flex items-end">
        <div className="relative w-full rounded-2xl bg-slate-900 border border-slate-700/80 focus-within:border-indigo-500/80 focus-within:ring-2 focus-within:ring-indigo-500/20 shadow-lg transition-all duration-200">
          <textarea
            ref={textareaRef}
            rows={1}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={disabled}
            placeholder={
              isConnecting
                ? 'Connecting to backend... (waking up free-tier server)'
                : isOffline
                ? 'Backend is offline. Please check connection...'
                : 'Ask NexusRAG about your documents... (Press Enter to send, Shift+Enter for new line)'
            }
            className="w-full resize-none bg-transparent px-4 py-3.5 pr-14 text-sm text-slate-100 placeholder-slate-500 focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed max-h-44"
          />

          <button
            type="submit"
            disabled={disabled || !input.trim()}
            className="absolute right-2.5 bottom-2.5 p-2 rounded-xl bg-indigo-600 text-white hover:bg-indigo-500 disabled:opacity-30 disabled:hover:bg-indigo-600 disabled:cursor-not-allowed transition-all duration-200 shadow-sm flex items-center justify-center cursor-pointer"
            title="Send question (Enter)"
            aria-label="Send message"
          >
            {disabled ? (
              <div className="w-4 h-4 border-2 border-white/40 border-t-white rounded-full animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </button>
        </div>
      </form>
      <div className="flex justify-between items-center px-2 pt-1.5 text-[11px] text-slate-500">
        <span>Use Shift + Enter for multi-line queries</span>
        <span className="flex items-center space-x-1">
          <CornerDownLeft className="w-3 h-3" />
          <span>Enter to send</span>
        </span>
      </div>
    </div>
  );
};

export default ChatInput;

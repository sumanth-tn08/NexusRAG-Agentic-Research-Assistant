import React from 'react';
import ReactMarkdown from 'react-markdown';
import { User, Bot, Layers } from 'lucide-react';
import type { ChatMessage as ChatMessageType } from '../types';
import SourceCard from './SourceCard';

interface ChatMessageProps {
  message: ChatMessageType;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`flex w-full mb-6 ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`flex items-start max-w-[85%] md:max-w-[75%] space-x-3.5 ${isUser ? 'flex-row-reverse space-x-reverse' : 'flex-row'}`}>
        {/* Avatar */}
        <div
          className={`w-8 h-8 rounded-xl flex items-center justify-center flex-shrink-0 mt-0.5 shadow-md ${
            isUser
              ? 'bg-gradient-to-tr from-indigo-600 to-violet-600 text-white shadow-indigo-500/20'
              : 'bg-slate-800 border border-slate-700 text-indigo-400'
          }`}
        >
          {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
        </div>

        {/* Message bubble */}
        <div className="flex flex-col min-w-0">
          <div className="flex items-center space-x-2 mb-1 px-1">
            <span className={`text-xs font-medium ${isUser ? 'text-indigo-400 ml-auto' : 'text-slate-400'}`}>
              {isUser ? 'You' : 'NexusRAG'}
            </span>
            <span className="text-[10px] text-slate-500">{message.timestamp}</span>
          </div>

          <div
            className={`p-4 rounded-2xl text-sm leading-relaxed shadow-sm overflow-hidden ${
              isUser
                ? 'bg-indigo-600 text-white rounded-tr-sm selection:bg-indigo-700 selection:text-white'
                : 'bg-slate-900 border border-slate-800 text-slate-200 rounded-tl-sm'
            }`}
          >
            {isUser ? (
              <p className="whitespace-pre-wrap break-words">{message.content}</p>
            ) : (
              <div className="prose prose-invert max-w-none break-words text-slate-200 space-y-2">
                <ReactMarkdown
                  components={{
                    h1: ({ children }) => <h1 className="text-xl font-bold text-slate-100 my-2">{children}</h1>,
                    h2: ({ children }) => <h2 className="text-lg font-semibold text-slate-100 my-2">{children}</h2>,
                    h3: ({ children }) => <h3 className="text-base font-semibold text-slate-200 my-1">{children}</h3>,
                    p: ({ children }) => <p className="leading-relaxed mb-2 last:mb-0">{children}</p>,
                    ul: ({ children }) => <ul className="list-disc pl-5 my-2 space-y-1">{children}</ul>,
                    ol: ({ children }) => <ol className="list-decimal pl-5 my-2 space-y-1">{children}</ol>,
                    li: ({ children }) => <li className="text-slate-300">{children}</li>,
                    strong: ({ children }) => <strong className="font-semibold text-indigo-300">{children}</strong>,
                    em: ({ children }) => <em className="italic text-slate-300">{children}</em>,
                    code: ({ className, children, ...props }) => {
                      const isInline = !className && typeof children === 'string' && !children.includes('\n');
                      if (isInline) {
                        return (
                          <code className="bg-slate-800 text-indigo-300 px-1.5 py-0.5 rounded text-xs font-mono" {...props}>
                            {children}
                          </code>
                        );
                      }
                      return (
                        <div className="my-2 rounded-lg bg-slate-950/80 p-3 border border-slate-800/80 overflow-x-auto">
                          <code className="text-xs font-mono text-indigo-200" {...props}>
                            {children}
                          </code>
                        </div>
                      );
                    },
                    blockquote: ({ children }) => (
                      <blockquote className="border-l-2 border-indigo-500/50 pl-3 my-2 italic text-slate-400">
                        {children}
                      </blockquote>
                    ),
                  }}
                >
                  {message.content}
                </ReactMarkdown>
              </div>
            )}
          </div>

          {/* Sources Section */}
          {!isUser && message.sources && message.sources.length > 0 && (
            <div className="mt-3.5 pt-3 border-t border-slate-800/80">
              <div className="flex items-center space-x-1.5 mb-2.5 px-1">
                <Layers className="w-3.5 h-3.5 text-indigo-400" />
                <span className="text-xs font-medium uppercase tracking-wider text-slate-400">
                  Referenced Sources ({message.sources.length})
                </span>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {message.sources.map((src, idx) => (
                  <SourceCard key={`${idx}-${src.source}`} source={src} index={idx} />
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;

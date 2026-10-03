import React from 'react';
import { Bot, Sparkles } from 'lucide-react';

interface LoadingIndicatorProps {
  message?: string;
}

export const LoadingIndicator: React.FC<LoadingIndicatorProps> = ({
  message = 'NexusRAG is thinking...',
}) => {
  return (
    <div className="flex items-start space-x-3.5 max-w-2xl animate-fade-in">
      <div className="w-8 h-8 rounded-lg bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400 flex-shrink-0 mt-0.5">
        <Bot className="w-4 h-4 animate-pulse" />
      </div>

      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl rounded-tl-sm px-4 py-3 shadow-lg">
        <div className="flex items-center space-x-2 text-sm text-slate-300">
          <Sparkles className="w-3.5 h-3.5 text-indigo-400 animate-spin text-opacity-80" />
          <span className="font-medium tracking-wide text-slate-300">{message}</span>
          <div className="flex space-x-1 pl-1">
            <span className="w-1.5 h-1.5 bg-indigo-400 rounded-full animate-bounce [animation-delay:-0.3s]"></span>
            <span className="w-1.5 h-1.5 bg-indigo-400 rounded-full animate-bounce [animation-delay:-0.15s]"></span>
            <span className="w-1.5 h-1.5 bg-indigo-400 rounded-full animate-bounce"></span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoadingIndicator;

import React from 'react';
import { FileText, Bookmark } from 'lucide-react';
import type { Source } from '../types';

interface SourceCardProps {
  source: Source;
  index: number;
}

export const SourceCard: React.FC<SourceCardProps> = ({ source, index }) => {
  const rawText = source.source || '';
  
  // Format source text: often in format "filename.pdf, Page X" or "filename.pdf"
  let docName = rawText;
  let pageInfo = '';

  if (rawText.includes(',')) {
    const parts = rawText.split(',');
    docName = parts[0].trim();
    pageInfo = parts.slice(1).join(',').trim();
  }

  return (
    <div className="group relative flex items-start space-x-3 p-3 rounded-xl bg-slate-900/70 border border-slate-800/80 hover:border-indigo-500/40 hover:bg-slate-900 transition-all duration-200 shadow-sm text-left">
      <div className="p-2 rounded-lg bg-indigo-500/10 text-indigo-400 group-hover:bg-indigo-500/20 transition-colors flex-shrink-0">
        <FileText className="w-4 h-4" />
      </div>

      <div className="flex-1 min-w-0">
        <div className="flex items-center space-x-1.5 mb-0.5">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-indigo-400/90">
            Source [{index + 1}]
          </span>
        </div>
        <p className="text-xs font-medium text-slate-200 truncate" title={docName}>
          {docName}
        </p>
        {pageInfo && (
          <div className="flex items-center mt-1 text-[11px] text-slate-400">
            <Bookmark className="w-3 h-3 mr-1 text-slate-500 flex-shrink-0" />
            <span className="truncate">{pageInfo}</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default SourceCard;

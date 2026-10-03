import React from 'react';
import { FileText, Layers, Check, Trash2 } from 'lucide-react';
import type { UploadedDocument } from '../types';

interface DocumentListProps {
  documents: UploadedDocument[];
  selectedIds: string[];
  onToggleSelect: (documentId: string) => void;
  onDelete: (documentId: string) => void;
}

export const DocumentList: React.FC<DocumentListProps> = ({ documents, selectedIds, onToggleSelect, onDelete }) => {
  if (documents.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center p-6 text-center rounded-xl border border-dashed border-slate-800 bg-slate-900/40">
        <FileText className="w-8 h-8 text-slate-600 mb-2" />
        <p className="text-xs font-medium text-slate-400">No documents yet</p>
        <p className="text-[11px] text-slate-500 mt-1 max-w-[180px]">
          Upload a PDF to ground the agentic research assistant in your notes.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {documents.map((doc) => {
        const isSelected = selectedIds.includes(doc.document_id);
        return (
          <div
            key={doc.document_id}
            className="group flex items-start space-x-3 p-2.5 rounded-xl bg-slate-900/70 border border-slate-800/80 hover:border-slate-700 hover:bg-slate-900 transition-all duration-150"
          >
            <button
              type="button"
              onClick={() => onToggleSelect(doc.document_id)}
              className={`w-4 h-4 rounded border-2 flex items-center justify-center transition-colors cursor-pointer mt-0.5 flex-shrink-0 ${
                isSelected ? 'bg-indigo-600 border-indigo-600' : 'bg-slate-800 border-slate-600 hover:border-slate-500'
              }`}
              aria-label={isSelected ? `Deselect ${doc.filename}` : `Select ${doc.filename}`}
            >
              {isSelected && <Check className="w-3 h-3 text-white stroke-[3]" />}
            </button>
            <div
              className="p-2 rounded-lg bg-red-500/10 text-red-400 group-hover:bg-red-500/15 transition-colors flex-shrink-0 mt-0.5 cursor-pointer"
              onClick={() => onToggleSelect(doc.document_id)}
            >
              <FileText className="w-4 h-4" />
            </div>
            <div
              className="flex-1 min-w-0 cursor-pointer"
              onClick={() => onToggleSelect(doc.document_id)}
            >
              <p className="text-xs font-medium text-slate-200 truncate" title={doc.filename}>
                {doc.filename}
              </p>
              <div className="flex items-center space-x-2 mt-1">
                <span className="inline-flex items-center text-[10px] font-mono text-indigo-300 bg-indigo-950/60 border border-indigo-800/40 px-1.5 py-0.5 rounded">
                  <Layers className="w-2.5 h-2.5 mr-1 text-indigo-400" />
                  {doc.chunks} chunks
                </span>
                {doc.uploadedAt && (
                  <span className="text-[10px] text-slate-500">{doc.uploadedAt}</span>
                )}
              </div>
            </div>
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                onDelete(doc.document_id);
              }}
              className="text-slate-400 hover:text-red-400 transition-colors cursor-pointer p-1 rounded hover:bg-slate-800 flex-shrink-0"
              aria-label={`Delete ${doc.filename}`}
              title={`Delete ${doc.filename}`}
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        );
      })}
    </div>
  );
};

export default DocumentList;

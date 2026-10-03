import React from 'react';
import { Sparkles, Files, X, BookOpen } from 'lucide-react';
import DocumentUpload from './DocumentUpload';
import DocumentList from './DocumentList';
import type { UploadedDocument } from '../types';

interface SidebarProps {
  documents: UploadedDocument[];
  onUploadSuccess: (doc: UploadedDocument) => void;
  isOpen: boolean;
  onClose: () => void;
  isBackendConnected: boolean;
  selectedIds: string[];
  onToggleSelect: (documentId: string) => void;
  onDelete: (documentId: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  documents,
  onUploadSuccess,
  isOpen,
  onClose,
  isBackendConnected,
  selectedIds,
  onToggleSelect,
  onDelete,
}) => {
  return (
    <>
      {/* Mobile Backdrop overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/60 backdrop-blur-xs md:hidden"
          onClick={onClose}
          aria-hidden="true"
        />
      )}

      {/* Sidebar container */}
      <aside
        className={`fixed md:static inset-y-0 left-0 z-50 w-72 md:w-80 bg-slate-950 border-r border-slate-800/80 flex flex-col transition-transform duration-300 ease-in-out ${
          isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
        }`}
      >
        {/* Brand Header */}
        <div className="flex items-center justify-between p-4 border-b border-slate-800/80">
          <div className="flex items-center space-x-2.5">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-violet-500 flex items-center justify-center text-white shadow-md shadow-indigo-500/20">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-base font-bold tracking-tight text-white flex items-center gap-1.5">
                NexusRAG
              </h1>
              <p className="text-[11px] text-slate-400 font-medium">Research Assistant</p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="md:hidden p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            aria-label="Close sidebar"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Upload Action */}
        <div className="p-4 border-b border-slate-800/60">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
              <BookOpen className="w-3.5 h-3.5 text-indigo-400" />
              Document Store
            </span>
          </div>
          <DocumentUpload
            onUploadSuccess={onUploadSuccess}
            disabled={!isBackendConnected}
          />
        </div>

        {/* Documents Scrollable List */}
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          <div className="flex items-center justify-between mb-1">
            <div className="flex items-center space-x-1.5 text-xs font-semibold uppercase tracking-wider text-slate-400">
              <Files className="w-3.5 h-3.5 text-indigo-400" />
              <span>Loaded Documents</span>
            </div>
            <span className="text-[11px] font-mono font-medium text-slate-500 bg-slate-900 px-2 py-0.5 rounded-full border border-slate-800">
              {documents.length}
            </span>
          </div>

          <DocumentList documents={documents} selectedIds={selectedIds} onToggleSelect={onToggleSelect} onDelete={onDelete} />
        </div>

        {/* Sidebar Footer info */}
        <div className="p-3.5 border-t border-slate-800/80 bg-slate-950/60">
          <div className="text-[11px] text-slate-500 flex items-center justify-between">
            <span>RAG Document Store</span>
            <span className="text-slate-400 font-mono text-[10px]">Session scoped</span>
          </div>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;

import React, { useRef, useState } from 'react';
import { CheckCircle2, AlertCircle, Loader2, FileUp } from 'lucide-react';
import { uploadDocument } from '../services/api';
import type { UploadedDocument } from '../types';

interface DocumentUploadProps {
  onUploadSuccess: (doc: UploadedDocument) => void;
  disabled?: boolean;
}

type UploadStatus = 'idle' | 'uploading' | 'processing' | 'success' | 'error';

export const DocumentUpload: React.FC<DocumentUploadProps> = ({
  onUploadSuccess,
  disabled = false,
}) => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [status, setStatus] = useState<UploadStatus>('idle');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [recentUpload, setRecentUpload] = useState<UploadedDocument | null>(null);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Reset previous feedback
    setErrorMessage(null);
    setRecentUpload(null);

    // Validate PDF
    if (file.type !== 'application/pdf' && !file.name.toLowerCase().endsWith('.pdf')) {
      setStatus('error');
      setErrorMessage('Only PDF files are supported.');
      if (fileInputRef.current) fileInputRef.current.value = '';
      return;
    }

    try {
      setStatus('uploading');
      
      // Simulate transitional UI feedback for processing
      const processingTimer = setTimeout(() => {
        setStatus('processing');
      }, 1000);

      const doc = await uploadDocument(file);
      clearTimeout(processingTimer);

      setStatus('success');
      setRecentUpload(doc);
      onUploadSuccess(doc);

      // Revert status to idle after 3.5 seconds
      setTimeout(() => {
        setStatus('idle');
      }, 3500);
    } catch (err: any) {
      setStatus('error');
      setErrorMessage(
        err.response?.data?.detail || 'Upload failed. Please try again.'
      );
      setTimeout(() => {
        setStatus((prev) => (prev === 'error' ? 'idle' : prev));
        setErrorMessage(null);
      }, 6000);
    } finally {
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleClick = () => {
    if (status === 'uploading' || status === 'processing' || disabled) return;
    fileInputRef.current?.click();
  };

  return (
    <div className="w-full">
      <input
        ref={fileInputRef}
        type="file"
        accept="application/pdf,.pdf"
        className="hidden"
        onChange={handleFileChange}
      />

      <button
        onClick={handleClick}
        disabled={status === 'uploading' || status === 'processing' || disabled}
        className={`w-full group relative flex items-center justify-center space-x-2 py-2.5 px-4 rounded-xl text-sm font-medium transition-all duration-200 border cursor-pointer ${
          status === 'uploading' || status === 'processing'
            ? 'bg-slate-800/80 border-indigo-500/40 text-indigo-300 cursor-wait'
            : status === 'success'
            ? 'bg-emerald-950/40 border-emerald-500/50 text-emerald-300'
            : status === 'error'
            ? 'bg-red-950/40 border-red-500/50 text-red-300'
            : 'bg-indigo-600 hover:bg-indigo-500 text-white border-transparent shadow-md shadow-indigo-600/20 active:scale-[0.99]'
        }`}
      >
        {status === 'uploading' && (
          <>
            <Loader2 className="w-4 h-4 animate-spin text-indigo-400" />
            <span>Uploading...</span>
          </>
        )}

        {status === 'processing' && (
          <>
            <Loader2 className="w-4 h-4 animate-spin text-indigo-400" />
            <span>Processing...</span>
          </>
        )}

        {status === 'success' && (
          <>
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            <span>Uploaded successfully</span>
          </>
        )}

        {status === 'error' && (
          <>
            <AlertCircle className="w-4 h-4 text-red-400" />
            <span>Try Upload Again</span>
          </>
        )}

        {status === 'idle' && (
          <>
            <FileUp className="w-4 h-4 group-hover:-translate-y-0.5 transition-transform" />
            <span>+ Upload PDF</span>
          </>
        )}
      </button>

      {/* Success banner with chunks summary */}
      {status === 'success' && recentUpload && (
        <div className="mt-2.5 p-2.5 rounded-lg bg-emerald-950/30 border border-emerald-800/50 text-xs text-emerald-300 animate-fade-in flex items-center justify-between">
          <div className="truncate font-medium">✓ {recentUpload.filename}</div>
          <div className="ml-2 font-mono text-[11px] text-emerald-400/80 bg-emerald-900/40 px-1.5 py-0.5 rounded flex-shrink-0">
            {recentUpload.chunks} chunks
          </div>
        </div>
      )}

      {/* Error alert */}
      {errorMessage && status === 'error' && (
        <div className="mt-2.5 p-2.5 rounded-lg bg-red-950/30 border border-red-800/50 text-xs text-red-300 flex items-start space-x-2 animate-fade-in">
          <AlertCircle className="w-4 h-4 text-red-400 flex-shrink-0 mt-0.5" />
          <span>{errorMessage}</span>
        </div>
      )}
    </div>
  );
};

export default DocumentUpload;

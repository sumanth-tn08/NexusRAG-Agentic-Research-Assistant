import axios from 'axios';
import type { UploadedDocument, ChatRequest, ChatResponse } from '../types';

const api = axios.create({
  baseURL: '/api',
  timeout: 120000, // 2 mins for LLM / ingestion response
});

export const checkHealth = async (): Promise<boolean> => {
  try {
    const res = await api.get('/health');
    return res.status === 200;
  } catch {
    return false;
  }
};

export const uploadDocument = async (file: File): Promise<UploadedDocument> => {
  const formData = new FormData();
  formData.append('file', file);

  const res = await api.post<UploadedDocument & { message?: string }>('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  console.log('UPLOAD RESPONSE:', {
    document_id: res.data.document_id,
    filename: res.data.filename,
    chunks: res.data.chunks,
  });

  return {
    document_id: res.data.document_id,
    filename: res.data.filename,
    chunks: res.data.chunks,
    uploadedAt: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
  };
};

export const sendChatMessage = async (question: string, sessionId: string, documentIds: string[]): Promise<ChatResponse> => {
  const payload: ChatRequest = {
    question,
    session_id: sessionId,
    document_ids: documentIds,
  };

  console.log('CHAT REQUEST:', {
    question: payload.question,
    session_id: payload.session_id,
    document_ids: payload.document_ids,
  });

  const res = await api.post<ChatResponse>('/chat', payload);
  return res.data;
};

export const deleteSession = async (sessionId: string): Promise<void> => {
  await api.delete(`/sessions/${sessionId}`);
};

// Delete a document by ID
export const deleteDocument = async (documentId: string): Promise<void> => {
  console.log('DELETE REQUEST:', {
    document_id: documentId,
  });

  await api.delete(`/documents/${documentId}`);
};


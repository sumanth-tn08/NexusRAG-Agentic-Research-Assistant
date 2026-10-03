export interface UploadedDocument {
  document_id: string;
  filename: string;
  chunks: number;
  uploadedAt?: string;
}

export interface Source {
  source: string;
}

export interface ChatRequest {
  question: string;
  session_id: string;
  document_ids: string[];
}

export interface ChatResponse {
  answer: string;
  sources: Source[];
  session_id: string;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: Source[];
  timestamp: string;
}

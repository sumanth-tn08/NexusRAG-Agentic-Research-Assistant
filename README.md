# NexusRAG — Agentic Research Assistant

NexusRAG is an AI-powered document research assistant that lets users upload PDF documents, ask questions about them, and receive answers grounded in the uploaded content with source and page references.

The project was built as a learning project to understand **RAG, agentic workflows, vector databases, embeddings, document retrieval, and full-stack deployment**.

---

## Features

- 📄 Upload PDF documents
- 🔎 Semantic document search
- 🤖 Agentic question answering with LangGraph
- 🧠 Conversational session memory
- 📚 Multi-document selection
- 🎯 Document-specific retrieval
- 🔗 Source citations with page numbers
- 🧮 Calculator tool for mathematical questions
- 🗑️ Delete uploaded documents
- ⚡ Fast document embeddings using FastEmbed
- ☁️ Qdrant Cloud vector database
- 🌐 React frontend
- 🚀 FastAPI backend

---

## Architecture

```text
                    ┌──────────────────────┐
                    │     React Frontend   │
                    │  TypeScript + Vite   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      FastAPI API     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     LangGraph Agent  │
                    └───────┬───────┬──────┘
                            │       │
                 ┌──────────┘       └──────────┐
                 ▼                             ▼
        ┌─────────────────┐          ┌─────────────────┐
        │ Document Search │          │    Calculator   │
        └────────┬────────┘          └─────────────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ Qdrant Cloud    │
        │ Vector Database │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ Groq LLM        │
        └─────────────────┘
```

---

## RAG Pipeline

```text
PDF Upload
    ↓
PyMuPDF
    ↓
Text Extraction
    ↓
Recursive Text Splitting
    ↓
FastEmbed
(BAAI/bge-small-en-v1.5)
    ↓
Qdrant Cloud
    ↓
Similarity Search
    ↓
Reranking
    ↓
Relevant Document Chunks
    ↓
LangGraph Agent
    ↓
Groq LLM
    ↓
Answer + Sources
```

---

## Tech Stack

### Frontend

- React
- TypeScript
- Vite
- Axios
- Tailwind CSS
- Lucide React

### Backend

- Python
- FastAPI
- Uvicorn
- LangChain
- LangGraph
- LangChain OpenAI-compatible integration
- PyMuPDF

### AI / RAG

- Groq
- FastEmbed
- BAAI/bge-small-en-v1.5
- Qdrant Cloud
- MS MARCO MiniLM reranker

### Deployment

- Vercel — frontend
- Render — backend
- Qdrant Cloud — vector database

---

## Project Structure

```text
NexusRAG/
│
├── backend/
│   ├── app/
│   │   ├── agent/
│   │   ├── rag/
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── render.yaml
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── types/
│   │   └── App.tsx
│   │
│   └── package.json
│
├── .gitignore
└── README.md
```

---

## Backend API

### Health Check

```http
GET /health
```

### Upload PDF

```http
POST /upload
```

Returns a generated document ID and number of processed chunks.

### Chat

```http
POST /chat
```

Example request:

```json
{
  "question": "What is mentioned in the document?",
  "session_id": "default",
  "document_ids": [
    "document-uuid"
  ]
}
```

### Delete Document

```http
DELETE /documents/{document_id}
```

### Delete Session

```http
DELETE /sessions/{session_id}
```

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/sumanth-tn08/NexusRAG-Agentic-Research-Assistant.git
cd NexusRAG-Agentic-Research-Assistant
```

### 2. Backend

```bash
cd backend

python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend normally runs at:

```text
http://localhost:5173
```

For production, the frontend uses:

```env
VITE_API_URL=https://nexusrag-agentic-research-assistant.onrender.com
```

---

## Environment Variables

### Backend

```env
GROQ_API_KEY=
QDRANT_URL=
QDRANT_API_KEY=
```

### Frontend

```env
VITE_API_URL=
```

Never commit `.env` files or API keys to GitHub.

---

## Example Workflow

1. Open NexusRAG.
2. Upload a PDF.
3. Select the document.
4. Ask a question about the document.
5. NexusRAG searches the relevant document chunks.
6. The agent generates an answer.
7. The UI displays the referenced source documents and page numbers.
8. Multiple documents can be selected for broader research.
9. Documents can be deleted from the vector store.

Example:

```text
User:
"What is the person's name mentioned in the PDF?"

NexusRAG:
"The person named in the document is S Mahamad Jaish."

Sources:
- document.pdf — Page 1
- document.pdf — Page 2
```

---

## What I Learned

This project was built to learn the practical workflow behind modern RAG applications.

### RAG

- Document loading
- Text chunking
- Embeddings
- Vector databases
- Similarity search
- Metadata filtering
- Reranking
- Context retrieval

### Agentic AI

- LangGraph
- Agent/tool workflows
- Tool calling
- Calculator tools
- Routing user questions to appropriate tools

### Backend

- FastAPI
- REST APIs
- File uploads
- Session-based memory
- CORS
- Async/background processing

### Frontend

- React components
- TypeScript
- API integration
- Document state management
- Loading/error states
- Multi-document selection

### Deployment

- Git and GitHub
- Vercel
- Render
- Environment variables
- CORS configuration
- Production debugging

---

## Deployment

The project was deployed using:

```text
Frontend  → Vercel
Backend   → Render
Vector DB → Qdrant Cloud
```

Production services:

- Frontend: `https://nexus-rag-agentic-research-assistant.vercel.app`
- Backend: `https://nexusrag-agentic-research-assistant.onrender.com`

The Render free tier may spin down the backend after inactivity. Because of this, the first request after inactivity can take longer than a normal request.

---

## Known Limitations

This is a learning/project deployment rather than a production system.

- Render free-tier instances can sleep after inactivity.
- The backend keeps conversational memory in process memory.
- Uploaded documents are stored in the Qdrant collection rather than a permanent file-storage system.
- Large PDFs can require significant memory during embedding.
- Authentication and user accounts are not implemented.
- The system is designed primarily for PDF-based document research.
- Production reliability depends partly on the free-tier hosting limits.

---

## Why This Project?

The goal of NexusRAG was not simply to build a chatbot.

The goal was to understand how an AI application can connect:

```text
Documents
    ↓
Embeddings
    ↓
Vector Database
    ↓
Retrieval
    ↓
Reranking
    ↓
Agent
    ↓
LLM
    ↓
Grounded Answer
```

This project represents a practical step from traditional web development toward **RAG and Agentic AI application development**.

---

## Future Improvements

Possible future improvements include:

- Better document-grounding controls
- More reliable production deployment
- Streaming responses
- More document formats
- Authentication and user-specific document collections
- Persistent conversation history
- Better evaluation of retrieval quality
- Background document processing
- Improved observability and error handling

---

## Author

**Sumanth**

B.Tech Computer Science & Engineering

This project was created as part of my learning journey in:

- Generative AI
- RAG
- Agentic AI
- LangChain
- LangGraph
- Vector Databases
- Full-Stack AI Applications

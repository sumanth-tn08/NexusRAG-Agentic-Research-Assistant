import os
import shutil
import tempfile
import uuid

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)

from pydantic import BaseModel

from app.agent.service import (
    run_agent,
    memory
)

from app.rag.upload import (
    process_uploaded_file
)

from app.rag.vector_store import delete_document

app = FastAPI(
    title="NexusRAG API",
    description="Agentic RAG Research Assistant",
    version="1.0.0"
)


class ChatRequest(BaseModel):

    question: str

    session_id: str = "default"

    document_ids: list[str] = []

class Source(BaseModel):

    source: str


class ChatResponse(BaseModel):

    answer: str

    sources: list[Source]

    session_id: str


@app.get("/")
def root():

    return {
        "message": "NexusRAG API is running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest
):

    result = run_agent(
        question=request.question,
        session_id=request.session_id,
        document_ids=request.document_ids
    )

    answer = result["answer"]

    sources = []

    for message in result["messages"]:

        if message.type != "tool":
            continue

        content = message.content

        for line in content.splitlines():

            if line.startswith("[SOURCE:"):

                source = (
                    line
                    .replace("[SOURCE:", "")
                    .replace("]", "")
                    .strip()
                )

                if source not in sources:

                    sources.append(source)

    return ChatResponse(
        answer=answer,
        sources=[
            Source(source=source)
            for source in sources
        ],
        session_id=request.session_id
    )


@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    # Only allow PDF files for now
    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    temp_path = None

    try:
        
        document_id = str(
            uuid.uuid4()
        )

        # Create temporary file
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            temp_path = temp_file.name

            shutil.copyfileobj(
                file.file,
                temp_file
            )

        # Process document
        chunk_count = process_uploaded_file(
            file_path=temp_path,
            document_id=document_id,
            filename=file.filename
        )

        return {
            "message": "Document uploaded successfully",
            "document_id": document_id,
            "filename": file.filename,
            "chunks": chunk_count
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        if temp_path and os.path.exists(temp_path):

            os.remove(temp_path)


@app.delete(
    "/sessions/{session_id}"
)
def clear_session(
    session_id: str
):

    memory.clear(
        session_id
    )

    return {
        "message": "Conversation cleared",
        "session_id": session_id
    }
    
@app.delete(
    "/documents/{document_id}"
)
def remove_document(
    document_id: str
):

    try:

        delete_document(
            document_id
        )

        return {
            "message": "Document deleted successfully",
            "document_id": document_id
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )    
  @app.get("/debug/qdrant")
def debug_qdrant():
    import os
    from qdrant_client import QdrantClient

    url = os.getenv("QDRANT_URL")
    key = os.getenv("QDRANT_API_KEY")

    result = {
        "url_configured": bool(url),
        "key_configured": bool(key),
    }

    try:
        client = QdrantClient(
            url=url,
            api_key=key
        )

        client.get_collections()

        result["qdrant_connection"] = "OK"

    except Exception as e:
        result["qdrant_connection"] = "FAILED"
        result["error_type"] = type(e).__name__
        result["error"] = str(e)

    return result      
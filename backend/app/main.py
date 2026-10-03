from fastapi import FastAPI
from pydantic import BaseModel

from app.agent.service import (
    run_agent,
    memory
)


app = FastAPI(
    title="NexusRAG API",
    description="Agentic RAG Research Assistant",
    version="1.0.0"
)


class ChatRequest(BaseModel):

    question: str

    session_id: str = "default"


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
        session_id=request.session_id
    )

    answer = result["answer"]

    sources = []

    # Extract source information from tool messages
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
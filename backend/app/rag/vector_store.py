import os

from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore

from app.rag.embeddings import get_embeddings
from app.rag.ingestion import load_and_split


load_dotenv()


COLLECTION_NAME = "nexusrag"


def add_document_to_qdrant(
    file_path: str,
    document_id: str,
    filename: str
):

    chunks = load_and_split(file_path)

    # Add application-level metadata
    for chunk in chunks:

        chunk.metadata["document_id"] = document_id
        chunk.metadata["filename"] = filename

    embeddings = get_embeddings()

    QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        collection_name=COLLECTION_NAME,
        batch_size=10
    )

    return len(chunks)
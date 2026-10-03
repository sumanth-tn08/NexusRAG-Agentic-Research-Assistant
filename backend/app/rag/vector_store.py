import os

from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore

from app.rag.embeddings import get_embeddings
from app.rag.ingestion import load_and_split
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchValue,
    FilterSelector
)

load_dotenv()


COLLECTION_NAME = "nexusrag"


def add_document_to_qdrant(
    file_path: str,
    document_id: str,
    filename: str
):

    chunks = load_and_split(file_path)

    for chunk in chunks:
        chunk.metadata["document_id"] = document_id
        chunk.metadata["filename"] = filename

    embeddings = get_embeddings()

    QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        collection_name="nexusrag",
        batch_size=10
    )

    return len(chunks)

def delete_document(
    document_id: str
):

    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )

    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=FilterSelector(
            filter=Filter(
                must=[
                    FieldCondition(
                        key="metadata.document_id",
                        match=MatchValue(
                            value=document_id
                        )
                    )
                ]
            )
        )
    )

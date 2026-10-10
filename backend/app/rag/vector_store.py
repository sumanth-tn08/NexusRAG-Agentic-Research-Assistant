import os

from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchValue,
    FilterSelector,
)

from app.rag.embeddings import get_embeddings
from app.rag.ingestion import load_and_split

from functools import lru_cache
import gc

load_dotenv()

COLLECTION_NAME = "nexusrag"


@lru_cache(maxsize=1)
def get_qdrant_client():
    return QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        timeout=60,
    )


@lru_cache(maxsize=1)
def get_vector_store():
    return QdrantVectorStore(
        client=get_qdrant_client(),
        collection_name=COLLECTION_NAME,
        embedding=get_embeddings(),
    )


def add_document_to_qdrant(
    file_path: str,
    document_id: str,
    filename: str,
):
    try:
        chunks = load_and_split(file_path)
        if not chunks:
            return 0

        # Safety cap to avoid exceeding Render's 512MB RAM limit
        MAX_CHUNKS = 150
        if len(chunks) > MAX_CHUNKS:
            chunks = chunks[:MAX_CHUNKS]

        for chunk in chunks:
            chunk.metadata["document_id"] = document_id
            chunk.metadata["filename"] = filename

        vector_store = get_vector_store()

        vector_store.add_documents(
            documents=chunks,
            batch_size=16
        )

        return len(chunks)
    finally:
        gc.collect()


def delete_document(
    document_id: str,
):
    client = get_qdrant_client()

    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=FilterSelector(
            filter=Filter(
                must=[
                    FieldCondition(
                        key="metadata.document_id",
                        match=MatchValue(
                            value=document_id,
                        ),
                    )
                ]
            )
        ),
    )
import os

from dotenv import load_dotenv
from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchAny,
    MatchValue,
)

from app.rag.vector_store import get_vector_store

load_dotenv()


def search_by_documents(
    question: str,
    document_ids: list[str],
    k: int = 4
):
    if not document_ids:
        return []

    vector_store = get_vector_store()

    qdrant_filter = Filter(
        must=[
            FieldCondition(
                key="metadata.document_id",
                match=MatchAny(
                    any=document_ids
                )
            )
        ]
    )

    documents = vector_store.similarity_search(
        query=question,
        k=k,
        filter=qdrant_filter
    )

    return documents


def similarity_search(question: str, k: int = 4):
    vector_store = get_vector_store()

    results = vector_store.similarity_search_with_score(
        question,
        k=k,
    )

    return results


def mmr_search(question: str, k: int = 4):
    vector_store = get_vector_store()

    results = vector_store.max_marginal_relevance_search(
        question,
        k=k,
        fetch_k=10,
        lambda_mult=0.5
    )

    return results


def filtered_search(
    question: str,
    source: str,
    k: int = 4
):
    vector_store = get_vector_store()

    qdrant_filter = Filter(
        must=[
            FieldCondition(
                key="metadata.source",
                match=MatchValue(
                    value=source
                )
            )
        ]
    )

    results = vector_store.similarity_search(
        question,
        k=k,
        filter=qdrant_filter
    )

    return results


if __name__ == "__main__":

    print("\n===== Similarity Search =====")

    results = similarity_search(
        "What is an operating system?"
    )

    for i, (document, score) in enumerate(results, start=1):

        print(f"\n--- Result {i} ---")
        print("Score:", score)
        print("Page:", document.metadata.get("page"))
        print(document.page_content[:300])

    print("\n===== MMR Search =====")

    results = mmr_search(
        "What is OOPS?"
    )

    for i, document in enumerate(results, start=1):

        print(f"\n--- Result {i} ---")
        print("Page:", document.metadata.get("page"))
        print(document.page_content[:300])        
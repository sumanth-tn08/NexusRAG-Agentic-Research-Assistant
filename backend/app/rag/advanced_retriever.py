from app.rag.search import search_by_documents
from app.rag.reranker import rerank_documents
from app.rag.compression import compress_documents


def retrieve_from_documents(
    question: str,
    document_ids: list[str]
):
    if not document_ids:
        return []

    # Retrieve fewer candidates to reduce memory usage.
    documents = search_by_documents(
        question=question,
        document_ids=document_ids,
        k=5
    )

    if not documents:
        return []

    # Rerank only the retrieved candidates.
    documents = rerank_documents(
        question=question,
        documents=documents,
        top_k=3
    )

    # Compress the final results.
    documents = compress_documents(
        question,
        documents
    )

    return documents
from app.rag.search import search_by_documents
from app.rag.reranker import Reranker


def retrieve_from_documents(
    question: str,
    document_ids: list[str]
):
    if not document_ids:
        return []

    documents = search_by_documents(
        question=question,
        document_ids=document_ids,
        k=5
    )

    if not documents:
        return []

    reranker = Reranker()

    documents = reranker.rerank(
        question=question,
        documents=documents,
        top_k=3
    )

    return documents
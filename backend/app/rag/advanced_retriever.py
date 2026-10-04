from app.rag.search import search_by_documents
from app.rag.reranker import Reranker
from app.rag.compressor import compress_documents


# Load reranker once and reuse it
reranker = Reranker()


def retrieve_from_documents(
    question: str,
    document_ids: list[str]
):
    documents = search_by_documents(
        question=question,
        document_ids=document_ids,
        k=8
    )

    if not documents:
        return []

    documents = reranker.rerank(
        question,
        documents,
        top_k=5
    )

    documents = compress_documents(
        question,
        documents
    )

    return documents
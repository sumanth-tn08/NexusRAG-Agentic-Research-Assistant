from app.rag.multi_query import multi_query_search
from app.rag.reranker import Reranker
from app.rag.compressor import compress_documents


def advanced_retrieve(question: str):

    # Step 1: Multi-query retrieval
    documents = multi_query_search(question)

    # Step 2: Reranking
    reranker = Reranker()

    documents = reranker.rerank(
        question,
        documents,
        top_k=5
    )

    # Step 3: Context compression
    documents = compress_documents(
        question,
        documents
    )

    return documents
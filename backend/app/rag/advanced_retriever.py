from app.rag.search import search_by_documents


def retrieve_from_documents(
    question: str,
    document_ids: list[str]
):
    """
    Retrieve relevant documents from the selected documents.

    Uses Qdrant similarity search directly to keep
    memory usage low on deployment.
    """

    if not document_ids:
        return []

    documents = search_by_documents(
        question=question,
        document_ids=document_ids,
        k=5
    )

    return documents
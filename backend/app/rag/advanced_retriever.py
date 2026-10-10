from app.rag.search import search_by_documents


def retrieve_from_documents(
    question: str,
    document_ids: list[str]
):
    documents = search_by_documents(
        question=question,
        document_ids=document_ids,
        k=4
    )

    return documents


def advanced_retrieve(question: str):
    from app.rag.search import similarity_search

    results = similarity_search(question, k=4)
    return [doc for doc, _ in results]
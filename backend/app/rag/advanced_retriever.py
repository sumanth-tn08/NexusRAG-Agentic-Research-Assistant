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
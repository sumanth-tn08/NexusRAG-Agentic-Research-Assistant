from langchain_core.tools import tool

from app.rag.advanced_retriever import (
    retrieve_from_documents
)


@tool
def search_documents(
    question: str,
    document_ids: list[str]
) -> str:
    """
    Search selected uploaded documents.

    question:
        User's document-related question.

    document_ids:
        IDs of the documents that should be searched.
    """

    if not document_ids:
        return "No documents are currently selected."

    documents = retrieve_from_documents(
        question=question,
        document_ids=document_ids
    )

    if not documents:
        return (
            "No relevant information was found "
            "in the selected documents."
        )

    results = []

    for document in documents:

        source_name = document.metadata.get(
            "filename",
            document.metadata.get(
                "source",
                "Unknown"
            )
        )

        page = document.metadata.get(
            "page"
        )

        if page is not None:
            source_info = (
                f"{source_name}, Page {page + 1}"
            )
        else:
            source_info = source_name

        results.append(
            f"[SOURCE: {source_info}]\n"
            f"{document.page_content}"
        )

    return "\n\n".join(results)

@tool
def calculator(expression: str) -> str:
    """
    Calculate a mathematical expression.
    Use this tool for arithmetic calculations.
    """

    allowed_characters = (
        "0123456789"
        "+-*/().% "
    )

    if any(
        character not in allowed_characters
        for character in expression
    ):
        return "Invalid mathematical expression."

    try:

        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return str(result)

    except Exception:

        return "Unable to calculate the expression."
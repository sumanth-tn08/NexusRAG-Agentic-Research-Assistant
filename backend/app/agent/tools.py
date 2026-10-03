from langchain_core.tools import tool

from app.rag.advanced_retriever import advanced_retrieve


@tool
def search_documents(question: str) -> str:
    """
    Search the uploaded documents and return relevant information.

    Use this tool when the user's question should be answered
    from the uploaded documents.
    """

    documents = advanced_retrieve(question)

    if not documents:
        return "No relevant information was found in the documents."

    results = []

    for document in documents:

        source_name = document.metadata.get(
            "filename",
            document.metadata.get("source", "Unknown")
        )

        page = document.metadata.get(
            "page",
            None
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
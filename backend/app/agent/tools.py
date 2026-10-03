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

        source = document.metadata.get(
            "source",
            "Unknown"
        )

        page = document.metadata.get(
            "page",
            None
        )

        # Extract only the filename
        source_name = source.split("\\")[-1]
        source_name = source_name.split("/")[-1]

        if page is not None:
            source_info = f"{source_name}, Page {page + 1}"
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

    try:

        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return str(result)

    except Exception:

        return "Unable to calculate the expression."
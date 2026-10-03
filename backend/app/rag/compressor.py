from app.rag.llm import get_llm


def compress_documents(
    question: str,
    documents: list
):

    llm = get_llm()

    compressed_documents = []

    for document in documents:

        prompt = f"""
Extract only the information from the following
document chunk that is relevant to the question.

If nothing is relevant, return an empty response.

Question:
{question}

Document:
{document.page_content}

Relevant information:
"""

        response = llm.invoke(prompt)

        content = response.content.strip()

        if content:

            document.page_content = content

            compressed_documents.append(
                document
            )

    return compressed_documents
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.rag.retriever import get_retriever
from app.rag.llm import get_llm


def generate_queries(question: str):

    llm = get_llm()

    prompt = ChatPromptTemplate.from_template(
        """
Generate 3 different search queries for the user's question.

The queries should express the same information need
using different wording.

Return only the queries, one per line.

Question:
{question}
"""
    )

    response = llm.invoke(
        prompt.invoke({
            "question": question
        })
    )

    queries = response.content.strip().split("\n")

    return [
        query.strip("- ").strip()
        for query in queries
        if query.strip()
    ]


def multi_query_search(question: str):

    retriever = get_retriever()

    queries = generate_queries(question)

    all_documents = []

    for query in queries:

        documents = retriever.invoke(query)

        all_documents.extend(documents)

    # Remove duplicate chunks
    unique_documents = {}

    for document in all_documents:

        key = (
            document.metadata.get("source"),
            document.metadata.get("page"),
            document.page_content
        )

        unique_documents[key] = document

    return list(unique_documents.values())
from app.rag.llm import get_llm
from app.rag.prompt import get_rag_prompt
from app.rag.advanced_retriever import advanced_retrieve


def get_rag_chain():

    llm = get_llm()
    prompt = get_rag_prompt()

    def rag_pipeline(question: str):

        documents = advanced_retrieve(question)

        context = "\n\n".join(
            document.page_content
            for document in documents
        )

        messages = prompt.invoke(
            {
                "context": context,
                "question": question
            }
        )

        response = llm.invoke(messages)

        return response.content, documents

    return rag_pipeline
from app.rag.llm import get_llm
from app.rag.prompt import get_rag_prompt
from app.rag.advanced_retriever import advanced_retrieve
from app.rag.memory import ConversationMemory
from app.rag.query_rewriter import rewrite_question


def get_rag_chain():

    llm = get_llm()
    prompt = get_rag_prompt()

    memory = ConversationMemory()

    def rag_pipeline(question: str):

        history_messages = memory.get_messages()

        history = "\n".join(
            f"{message.type}: {message.content}"
            for message in history_messages
        )

        # Understand the question using conversation history
        search_question = rewrite_question(
            question,
            history
        )

        # Retrieve relevant documents
        documents = advanced_retrieve(
            search_question
        )

        context = "\n\n".join(
            document.page_content
            for document in documents
        )

        messages = prompt.invoke(
            {
                "history": history,
                "context": context,
                "question": question
            }
        )

        response = llm.invoke(messages)

        answer = response.content

        # Store conversation
        memory.add_user_message(question)
        memory.add_ai_message(answer)

        return answer, documents

    return rag_pipeline
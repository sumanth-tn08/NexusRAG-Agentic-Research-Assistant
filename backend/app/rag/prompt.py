from langchain_core.prompts import ChatPromptTemplate

def get_rag_prompt():
    prompt = ChatPromptTemplate.from_template(
    """
    You are NexusRAG, an AI research assistant.

    Answer the user's question using only the provided context.

    If the answer cannot be found in the context, say:
    "I couldn't find the answer in the provided documents.
        
    Do not makeup information

    Conversation history:
    {history}

    Document Context:
    {context}

    Current Question:
    {question}

    Answer:
        """
            
    )
    return prompt
    
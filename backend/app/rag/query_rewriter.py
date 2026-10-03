from app.rag.llm import get_llm


def rewrite_question(question: str, history: str):

    llm = get_llm()

    prompt = f"""
Rewrite the user's current question into a
standalone search query.

Use the conversation history to resolve references
such as "it", "they", "this", "that", etc.

If the question is already standalone,
return it unchanged.

Return ONLY the rewritten search query.

Conversation history:
{history}

Current question:
{question}
"""

    response = llm.invoke(prompt)

    return response.content.strip()
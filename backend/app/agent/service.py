from langchain_core.messages import HumanMessage

from app.agent.graph import graph
from app.agent.memory import SessionMemory


memory = SessionMemory()


def run_agent(
    question: str,
    session_id: str,
    document_ids: list[str]
):

    history = memory.get_messages(
        session_id
    )

    agent_question = f"""
User question:
{question}

Selected document IDs:
{document_ids}

When using search_documents, pass exactly these
document IDs to the document_ids argument.
"""

    messages = history + [
        HumanMessage(
            content=agent_question
        )
    ]

    result = graph.invoke(
        {
            "messages": messages
        }
    )

    final_message = result["messages"][-1]

    memory.add_messages(
        session_id,
        [
            HumanMessage(content=question),
            final_message
        ]
    )

    return {
        "answer": final_message.content,
        "messages": result["messages"]
    }
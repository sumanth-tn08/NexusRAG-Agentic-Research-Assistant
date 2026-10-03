from langchain_core.messages import HumanMessage

from app.agent.graph import graph
from app.agent.memory import SessionMemory


memory = SessionMemory()


def run_agent(
    question: str,
    session_id: str
):

    history = memory.get_messages(
        session_id
    )

    messages = history + [
        HumanMessage(
            content=question
        )
    ]

    result = graph.invoke(
        {
            "messages": messages
        }
    )

    final_message = result["messages"][-1]

    # Save only the user question and final answer
    memory.add_messages(
        session_id,
        [
            HumanMessage(
                content=question
            ),
            final_message
        ]
    )

    return {
        "answer": final_message.content,
        "messages": result["messages"]
    }
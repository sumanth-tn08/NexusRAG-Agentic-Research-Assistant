from typing import Annotated
from typing_extensions import TypedDict

from langchain_core.messages import (
    BaseMessage,
    SystemMessage
)

from langgraph.graph import (
    StateGraph
)

from langgraph.graph.message import add_messages

from langgraph.prebuilt import (
    ToolNode,
    tools_condition
)

from app.agent.llm import get_agent_llm
from app.agent.tools import (
    search_documents,
    calculator
)


class AgentState(TypedDict):

    messages: Annotated[
        list[BaseMessage],
        add_messages
    ]


tools = [
    search_documents,
    calculator
]

llm = get_agent_llm()


SYSTEM_PROMPT = """
You are NexusRAG, an AI research assistant.

You can use these tools:

1. search_documents
   Use this when the user asks about information
   contained in the uploaded documents.

2. calculator
   Use this when the user asks for a mathematical
   calculation.

Rules:

- For questions about uploaded documents, always use
  search_documents before answering.
- For calculations, use calculator.
- For normal greetings or general conversation, you can
  answer directly.
- Do not invent facts from the uploaded documents.
- Base document answers only on the retrieved content.
- Keep answers clear and concise.
- When document sources are available, cite them like:

  [Source: filename, Page X]

- If multiple sources are relevant, include each relevant source.
"""


def agent_node(state: AgentState):

    messages = [
        SystemMessage(content=SYSTEM_PROMPT)
    ] + state["messages"]

    response = llm.invoke(messages)

    return {
        "messages": [response]
    }


tool_node = ToolNode(tools)


graph_builder = StateGraph(
    AgentState
)


graph_builder.add_node(
    "agent",
    agent_node
)

graph_builder.add_node(
    "tools",
    tool_node
)


graph_builder.set_entry_point(
    "agent"
)


graph_builder.add_conditional_edges(
    "agent",
    tools_condition
)


graph_builder.add_edge(
    "tools",
    "agent"
)


graph = graph_builder.compile()
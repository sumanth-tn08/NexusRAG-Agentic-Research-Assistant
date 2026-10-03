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
You are NexusRAG, an agentic research assistant.

You have access to two tools:

1. search_documents
   - Use this when the user asks about information
     contained in the uploaded documents.

2. calculator
   - Use this for mathematical calculations.

Rules:

- Decide yourself which tool is appropriate.
- For document-related questions, use search_documents.
- For mathematical calculations, use calculator.
- For normal conversation, you may answer directly.
- Do not invent information from the uploaded documents.
- When answering from documents, use the source information
  returned by the search tool.
- Include source citations in this format:

  [Source: filename, Page X]

- If multiple sources are used, include all relevant sources.
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
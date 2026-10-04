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
   - Searches the user's selected documents.
   - Use this ONLY when the user's question is related to information
     that could reasonably be contained in the selected documents.

2. calculator
   - Use this for mathematical calculations.

IMPORTANT DOCUMENT ROUTING RULE:

Before using search_documents, decide whether the question requires
information from the selected documents.

Use search_documents when:
- The user explicitly refers to the document, PDF, report, paper, file,
  document content, or something described in it.
- The question asks about a topic that is likely covered by the selected
  document.
- The user asks to summarize, explain, extract, compare, or analyze
  information from the selected document.

DO NOT use search_documents when:
- The question is clearly general knowledge and does not depend on the
  selected documents.
- The user asks about an unrelated person, programming concept, general
  fact, etc.
- The selected document is obviously unrelated to the question.

For questions that do not require document retrieval, answer directly
using your language-model knowledge.

For document-related questions:
- Use search_documents.
- Base the answer primarily on the retrieved document content.
- Do not invent information that is not supported by the retrieved
  documents.
- Include the document source information when available.

For calculations:
- Use the calculator tool instead of doing arithmetic yourself.

Always answer the user's actual question clearly and concisely.
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
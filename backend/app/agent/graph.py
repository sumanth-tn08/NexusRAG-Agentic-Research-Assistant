from typing import Annotated

from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict

from app.agent.llm import get_agent_llm
from app.agent.tools import search_documents, calculator

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

def agent_node(state:AgentState):
    
    response = llm.invoke(
        state["messages"]
    )
    return {
        "messages": [response]
    }
    
tool_node = ToolNode(tools)

graph_builder = StateGraph(AgentState)

graph_builder.add_node(
    "agent", agent_node
) 

graph_builder.add_node(
    "tools", tool_node
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
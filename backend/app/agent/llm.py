from app.rag.llm import get_llm
from app.agent.tools import search_documents, calculator

def get_agent_llm():
    
    llm = get_llm()
    
    tools = [
        search_documents,
        calculator
    ]
    
    llm_with_tools = llm.bind_tools(tools)
    
    return llm_with_tools
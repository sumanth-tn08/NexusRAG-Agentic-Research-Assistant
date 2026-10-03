from langchain_core.tools import tool

from app.rag.advanced_retriever import advanced_retrieve


@tool
def search_documents(question:str):
    """
     Search the uploaded documents and return relevant information.
    Use this when the user asks something that should be answered
    from the uploaded documents.
    """
    
    documents = advanced_retrieve(question)
    
    if not documents:
        return "No relevant information found in documents."
    
    context = "\n\n".join(
        document.page_content
        for document in documents
        
    )
    return context

@tool
def calculator(expression:str):
    """
    Calculate a mathematical expression
    Use this for arithmetic calculations.
    
    """
    
    try:
        
        result = eval(
            expression,
            {"__builtins__":{}},
        )
        return result(str)
    
    except Exception:
        return "Unable to calculate the given expression"
    
    
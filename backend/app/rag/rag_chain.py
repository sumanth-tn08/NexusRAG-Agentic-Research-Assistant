from app.rag.llm import get_llm
from app.rag.retriever import get_retriever
from app.rag.prompt import get_rag_prompt

def get_rag_chain():
    
    retriever = get_retriever()
    llm = get_llm()
    prompt = get_rag_prompt()
    
    def rag_pipeline(question:str):
        
        documents=retriever.invoke(question)
        
        context = "\n\n".join(
            document.page_content
            for document in documents
        )
        messages = prompt.invoke({
            "context" : context,
            "question" : question,
           })
        
        response = llm.invoke(messages)
        
        return response.content, documents
    return rag_pipeline
                                 
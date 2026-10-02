import os
from dotenv import load_dotenv

from langchain_qdrant import QdrantVectorStore
from app.rag.embeddings import get_embeddings

def get_retriever():
    
    embeddings = get_embeddings()
    
    vector_store = QdrantVectorStore.from_existing_collection(
        collection_name="nexusrag",
        embedding=embeddings,
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
    )
    
    retriever = vector_store.as_retriever(
        search_kwargs={
            "k":4
        }
    )
    return retriever
import os

from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore

from app.rag.embeddings import get_embeddings
from qdrant_client.models import Filter, FieldCondition, MatchValue

load_dotenv()

def get_vector_store():
    
    embeddings= get_embeddings()
    
    vector_store = QdrantVectorStore.from_existing_collection(
        embedding=embeddings,
        collection_name="nexusrag",
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"), 
    )
    
    return vector_store

def similarity_search(question:str, k: int=4):
    
    vector_store = get_vector_store()
    
    results = vector_store.similarity_search_with_score(
        question,
        k=k,
        
    )
    
    return results

def mmr_search(question: str, k: int = 4):

    vector_store = get_vector_store()

    results = vector_store.max_marginal_relevance_search(
        question,
        k=k,
        fetch_k=10,
        lambda_mult=0.5
    )

    return results

def filtered_search(
    question: str,
    source: str,
    k: int = 4
):

    vector_store = get_vector_store()

    qdrant_filter = Filter(
        must=[
            FieldCondition(
                key="metadata.source",
                match=MatchValue(
                    value=source
                )
            )
        ]
    )

    results = vector_store.similarity_search(
        question,
        k=k,
        filter=qdrant_filter
    )

    return results


if __name__ == "__main__":

    print("\n===== Similarity Search =====")

    results = similarity_search(
        "What is an operating system?"
    )

    for i, (document, score) in enumerate(results, start=1):

        print(f"\n--- Result {i} ---")
        print("Score:", score)
        print("Page:", document.metadata.get("page"))
        print(document.page_content[:300])

    print("\n===== MMR Search =====")

    results = mmr_search(
        "What is OOPS?"
    )

    for i, document in enumerate(results, start=1):

        print(f"\n--- Result {i} ---")
        print("Page:", document.metadata.get("page"))
        print(document.page_content[:300])
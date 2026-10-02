import os

from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore

from app.rag.embeddings import get_embeddings
from app.rag.ingestion import load_and_split

load_dotenv()


def create_vector_store(file_path: str):
    chunks = load_and_split(file_path)

    embeddings = get_embeddings()

    vector_store = QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        collection_name="nexusrag",
    )

    return vector_store


if __name__ == "__main__":
    vector_store = create_vector_store(
        "data/documents/OOPS Notes.pdf"
    )

    print("Documents successfully stored in Qdrant!")
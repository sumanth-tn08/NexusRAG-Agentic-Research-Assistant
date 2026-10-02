import os

from dotenv import load_dotenv
from qdrant_client import QdrantClient


load_dotenv()

url = os.getenv("QDRANT_URL")
api_key = os.getenv("QDRANT_API_KEY")

print("URL:", url)
print("API key exists:", bool(api_key))

client = QdrantClient(
    url=url,
    api_key=api_key
)

print("\nTesting Qdrant connection...")

collections = client.get_collections()

print("\nConnection successful!")
print(collections)
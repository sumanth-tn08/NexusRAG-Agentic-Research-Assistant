from functools import lru_cache

from langchain_community.embeddings.fastembed import FastEmbedEmbeddings


@lru_cache(maxsize=1)
def get_embeddings():
    return FastEmbedEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )
from langchain_huggingface import HuggingFaceEmbeddings


def get_embeddings():

    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )

    return embeddings


if __name__ == "__main__":

    embeddings = get_embeddings()

    vector = embeddings.embed_query(
        "What is an operating system?"
    )

    print("Vector dimensions:", len(vector))
    print("First 10 values:", vector[:10])
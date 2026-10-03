from langchain_community.embeddings.fastembed import FastEmbedEmbeddings


def get_embeddings():
    return FastEmbedEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )


if __name__ == "__main__":

    embeddings = get_embeddings()

    vector = embeddings.embed_query(
        "What is an operating system?"
    )

    print("Vector dimensions:", len(vector))
    print("First 10 values:", vector[:10])
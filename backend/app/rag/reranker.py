# Cross-encoder reranker removed to prevent exceeding Render's 512MB RAM limit.
# NexusRAG uses direct Qdrant similarity search instead.


class Reranker:

    def rerank(
        self,
        question: str,
        documents: list,
        top_k: int = 4
    ):
        if not documents:
            return []

        return documents[:top_k]
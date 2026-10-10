from functools import lru_cache
from fastembed.rerank.cross_encoder import TextCrossEncoder


@lru_cache(maxsize=1)
def get_reranker():
    return TextCrossEncoder(
        model_name="Xenova/ms-marco-MiniLM-L-6-v2"
    )


class Reranker:

    def rerank(
        self,
        question: str,
        documents: list,
        top_k: int = 3
    ):
        if not documents:
            return []

        model = get_reranker()

        texts = [
            document.page_content
            for document in documents
        ]

        scores = list(
            model.rerank(
                question,
                texts
            )
        )

        ranked = sorted(
            zip(documents, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            document
            for document, score in ranked[:top_k]
        ]
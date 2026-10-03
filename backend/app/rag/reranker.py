from fastembed.rerank.cross_encoder import TextCrossEncoder


class Reranker:

    def __init__(self):
        self.model = TextCrossEncoder(
            model_name="Xenova/ms-marco-MiniLM-L-6-v2"
        )

    def rerank(
        self,
        question: str,
        documents: list,
        top_k: int = 5
    ):

        texts = [
            document.page_content
            for document in documents
        ]

        scores = list(
            self.model.rerank(
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
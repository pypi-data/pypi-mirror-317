from ..types import TextEmbeddingResponse, EmbeddingUsage, Embedding


class VoyageAITextEmbeddingResponseAdapter(TextEmbeddingResponse):
    def __init__(self, response):
        super().__init__(
            id=None,
            object=None,
            model=None,
            usage=EmbeddingUsage(
                input_tokens=response.total_tokens,
                total_tokens=response.total_tokens,
            ),
            embeddings=[
                Embedding(
                    index=index,
                    data=data,
                )
                for index, data in enumerate(response.embeddings)
            ],
        )

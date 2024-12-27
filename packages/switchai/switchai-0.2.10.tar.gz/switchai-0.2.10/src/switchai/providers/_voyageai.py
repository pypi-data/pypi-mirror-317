from typing import Union, List

import voyageai

from ..base_client import BaseClient
from ..types import TextEmbeddingResponse, EmbeddingUsage, Embedding


class VoyageaiClientAdapter(BaseClient):
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.client = voyageai.Client(api_key=api_key)

    def embed(self, inputs: Union[str, List[str]]) -> TextEmbeddingResponse:
        response = self.client.embed(inputs, model=self.model_name)

        return VoyageaiTextEmbeddingResponseAdapter(response)


class VoyageaiTextEmbeddingResponseAdapter(TextEmbeddingResponse):
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

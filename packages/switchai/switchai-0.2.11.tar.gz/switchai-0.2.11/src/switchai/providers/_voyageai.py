from typing import Union, List

import voyageai
from PIL.Image import Image

from ..base_client import BaseClient
from ..types import EmbeddingResponse, EmbeddingUsage, Embedding
from ..utils import contains_image

SUPPORTED_MODELS = {
    "embed": {
        "text": [
            "voyage-3-large",
            "voyage-3",
            "voyage-3-lite",
            "voyage-code-3",
            "voyage-finance-2",
            "voyage-law-2",
            "voyage-code-2",
        ],
        "text_and_images": ["voyage-multimodal-3"],
    }
}

API_KEY_NAMING = "VOYAGE_API_KEY"


class VoyageaiClientAdapter(BaseClient):
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.client = voyageai.Client(api_key=api_key)

    def embed(self, inputs: Union[str, Image, List[Union[str, Image]]]) -> EmbeddingResponse:
        if contains_image(inputs):
            if (
                "text_and_images" not in SUPPORTED_MODELS["embed"]
                or self.model_name not in SUPPORTED_MODELS["embed"]["text_and_images"]
            ):
                raise ValueError(f"Model {self.model_name} does not support images.")

        if self.model_name in SUPPORTED_MODELS["embed"]["text"]:
            response = self.client.embed(inputs, model=self.model_name)

            return VoyageaiTextEmbeddingResponseAdapter(response)

        if self.model_name in SUPPORTED_MODELS["embed"]["text_and_images"]:
            if isinstance(inputs, str) or isinstance(inputs, Image):
                inputs = [[inputs]]
            else:
                inputs = [inputs]

            response = self.client.multimodal_embed(inputs, model=self.model_name)

            return VoyageaiTextAndImagesEmbeddingResponseAdapter(response)


class VoyageaiTextEmbeddingResponseAdapter(EmbeddingResponse):
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


class VoyageaiTextAndImagesEmbeddingResponseAdapter(EmbeddingResponse):
    def __init__(self, response):
        super().__init__(
            id=None,
            object=None,
            model=None,
            usage=EmbeddingUsage(
                input_tokens=response.text_tokens,
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

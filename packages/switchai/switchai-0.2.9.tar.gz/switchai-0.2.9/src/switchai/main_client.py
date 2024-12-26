import importlib
import os
from typing import List, Optional, Union

from .base_client import BaseClient
from .constants import SUPPORTED_MODELS, API_KEYS_NAMING
from .types import ChatResponse, TextEmbeddingResponse, TranscriptionResponse, ImageGenerationResponse, ChatChoice


class SwitchAI(BaseClient):
    """
    The SwitchAI client class.

    Args:
            provider (str): The name of the provider to use.
            model_name (str): The name of the model to use.
            api_key (str, optional): The API key to use, if not set it will be read from the environment variable. Defaults to None.
    """

    def __init__(self, provider: str, model_name: str, api_key: Optional[str] = None):
        self.provider = provider.lower()
        self.model_name = model_name

        self._validate_provider()
        self._validate_model()

        self.model_category = self._get_model_category(model_name)

        api_key = self._get_api_key(api_key)

        self.client = self._create_client(self.provider, self.model_name, api_key)

    def _validate_provider(self):
        if self.provider not in SUPPORTED_MODELS:
            supported_providers = ", ".join(SUPPORTED_MODELS.keys())
            raise ValueError(
                f"Provider '{self.provider}' is not supported. Supported providers are: {supported_providers}."
            )

    def _validate_model(self):
        provider_models = SUPPORTED_MODELS[self.provider]
        model_supported = any(self.model_name in models for models in provider_models.values())
        if not model_supported:
            alternative_providers = [
                p
                for p, models in SUPPORTED_MODELS.items()
                if any(self.model_name in m_list for m_list in models.values())
            ]
            if alternative_providers:
                alternatives = ", ".join(alternative_providers)
                raise ValueError(
                    f"Model '{self.model_name}' is not supported by provider '{self.provider}'. "
                    f"However, it is supported by: {alternatives}."
                )
            else:
                raise ValueError(f"Model '{self.model_name}' is not supported by any provider.")

    def _get_api_key(self, api_key: str | None) -> str:
        if api_key is None:
            api_key = os.environ.get(API_KEYS_NAMING[self.provider])
        if api_key is None:
            raise ValueError(
                f"The api_key client option must be set either by passing api_key to the client or by setting the {API_KEYS_NAMING[self.provider]} environment variable"
            )
        return api_key

    def chat(
        self,
        messages: List[str | ChatChoice | dict],
        temperature: float = 1.0,
        max_tokens: Optional[int] = None,
        n: int = 1,
        tools: Optional[List] = None,
    ) -> ChatResponse:
        if self.model_category != "chat":
            raise ValueError(f"Model '{self.model_name}' is not a chat model.")
        return self.client.chat(messages, temperature, max_tokens, n, tools)

    def embed(self, inputs: Union[str, List[str]]) -> TextEmbeddingResponse:
        if self.model_category != "embed":
            raise ValueError(f"Model '{self.model_name}' is not an embedding model.")
        return self.client.embed(inputs)

    def transcribe(self, audio_path: str, language: Optional[str] = None) -> TranscriptionResponse:
        if self.model_category != "transcribe":
            raise ValueError(f"Model '{self.model_name}' is not a speech-to-text model.")
        return self.client.transcribe(audio_path, language)

    def generate_image(self, prompt: str, n: int = 1) -> ImageGenerationResponse:
        if self.model_category != "generate_image":
            raise ValueError(f"Model '{self.model_name}' is not an image generation model.")
        return self.client.generate_image(prompt, n)

    @staticmethod
    def _create_client(provider: str, model_name: str, api_key: str):
        # Dynamically import the adapter module based on the provider name
        module_name = f"switchai.providers._{provider}"
        module = importlib.import_module(module_name)

        class_name = f"{provider.capitalize()}ClientAdapter"
        client_class = getattr(module, class_name)

        return client_class(model_name, api_key)

    @staticmethod
    def _get_model_category(model_name: str) -> str:
        for categories in SUPPORTED_MODELS.values():
            for category, model_list in categories.items():
                if model_name in model_list:
                    return category

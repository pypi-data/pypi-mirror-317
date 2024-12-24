import os
import warnings
from typing import Union, List

from .providers import *
from .types import ChatResponse, TextEmbeddingResponse, TranscriptionResponse


def showwarning(message, category, filename, lineno, file=None, line=None):
    print(f"{category.__name__}: {message}", file=file)


warnings.showwarning = showwarning

SUPPORTED_MODELS = {
    "openai": {
        "chat": ["gpt-4o-mini", "gpt-4o", "o1-preview", "o1-mini", "gpt-4"],
        "embed": ["text-embedding-ada-002", "text-embedding-3-small", "text-embedding-3-large"],
        "transcribe": ["whisper-1"],
    },
    "mistral": {
        "chat": [
            "mistral-large-latest",
            "mistral-small-latest",
            "pixtral-large-latest",
            "pixtral-12b",
            "open-mistral-7b",
            "open-mixtral-8x7b",
            "open-mixtral-8x22b",
        ],
        "embed": ["mistral-embed"],
    },
    "xai": {"chat": ["grok-beta", "grok-vision-beta"]},
    "anthropic": {"chat": ["claude-3-5-sonnet-latest", "claude-3-5-haiku-latest", "claude-3-opus-latest"]},
    "google": {
        "chat": ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.5-flash-8b"],
        "embed": ["models/text-embedding-004", "models/embedding-001"],
    },
    "deepgram": {
        "transcribe": [
            "nova-2",
            "nova",
            "enhanced",
            "base",
            "whisper-tiny",
            "whisper-small",
            "whisper-base",
            "whisper-medium",
            "whisper-large",
        ]
    },
    "voyageai": {
        "embed": [
            "voyage-3-large",
            "voyage-3",
            "voyage-3-lite",
            "voyage-code-3",
            "voyage-finance-2",
            "voyage-law-2",
            "voyage-code-2",
        ]
    },
}

API_KEYS_NAMING = {
    "openai": "OPENAI_API_KEY",
    "mistral": "MISTRAL_API_KEY",
    "xai": "XAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "google": "GEMINI_API_KEY",
    "deepgram": "DEEPGRAM_API_KEY",
    "voyageai": "VOYAGE_API_KEY",
}


class SwitchAI:
    """
    The SwitchAI client class.

    Args:
            provider (str): The name of the provider to use.
            model_name (str): The name of the model to use.
            api_key (str, optional): The API key to use, if not set it will be read from the environment variable. Defaults to None.
    """

    def __init__(self, provider: str, model_name: str, api_key: str | None = None):
        self.provider = provider.lower()
        self.model_name = model_name

        # Validate provider
        if provider not in SUPPORTED_MODELS:
            supported_providers = ", ".join(SUPPORTED_MODELS.keys())
            raise ValueError(
                f"Provider '{provider}' is not supported. Supported providers are: {supported_providers}."
            )

        # Validate model for the provider
        provider_models = SUPPORTED_MODELS[provider]
        model_supported = any(self.model_name in models for models in provider_models.values())
        if not model_supported:
            # Check if the model is supported by other providers
            alternative_providers = [
                p
                for p, models in SUPPORTED_MODELS.items()
                if any(self.model_name in m_list for m_list in models.values())
            ]
            if alternative_providers:
                alternatives = ", ".join(alternative_providers)
                raise ValueError(
                    f"Model '{self.model_name}' is not supported by provider '{provider}'. "
                    f"However, it is supported by: {alternatives}."
                )
            else:
                raise ValueError(f"Model '{self.model_name}' is not supported by any provider.")

        self.model_category = self.get_model_category(model_name)

        if api_key is None:
            api_key = os.environ.get(API_KEYS_NAMING[self.provider])
        if api_key is None:
            raise ValueError(
                f"The api_key client option must be set either by passing api_key to the client or by setting the {API_KEYS_NAMING[self.provider]} environment variable"
            )

        if self.provider == "openai":
            from openai import OpenAI

            self.client = OpenAI(api_key=api_key)

        elif self.provider == "xai":
            from openai import OpenAI

            self.client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")

        elif self.provider == "mistral":
            from mistralai import Mistral

            self.client = Mistral(api_key=api_key)

        elif self.provider == "anthropic":
            from anthropic import Anthropic

            self.client = Anthropic(api_key=api_key)

        elif self.provider == "google":
            import google.generativeai as genai

            genai.configure(api_key=api_key)
            # Delay the client creation until the chat method is called because a system prompt can't be set after the client is created
            self.client = None

        elif self.provider == "deepgram":
            from deepgram import DeepgramClient

            self.client = DeepgramClient(api_key=api_key)

        elif self.provider == "voyageai":
            import voyageai

            self.client = voyageai.Client(api_key=api_key)

    def chat(
        self, messages, temperature: float = 1.0, max_tokens: int | None = None, n: int = 1, tools: List = None
    ) -> ChatResponse:
        """
        Sends a chat request to the AI model and returns the response.

        Args:
            messages (list): A list of messages to send to the model.
            temperature (float, optional): What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. Defaults to 1.0.
            max_tokens (int, optional): The maximum number of tokens to generate. Defaults to None.
            n (int, optional): How many chat completion choices to generate for each input message. Defaults to 1.
            tools (List, optional): A list of tools the model may call.. Defaults to None.

        Returns:
            ChatResponse: The response from the model.
        """
        if self.model_category != "chat":
            raise ValueError(f"Model '{self.model_name}' is not a chat model.")

        if self.provider in ["openai", "xai"]:
            adapted_inputs = OpenAIChatInputsAdapter(messages, tools)

            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=adapted_inputs.messages,
                temperature=temperature,
                max_completion_tokens=max_tokens,
                n=n,
                tools=adapted_inputs.tools,
            )

            return OpenAIChatResponseAdapter(response)

        elif self.provider == "mistral":
            adapted_inputs = MistralChatInputsAdapter(messages, tools)

            response = self.client.chat.complete(
                model=self.model_name,
                messages=adapted_inputs.messages,
                temperature=temperature,
                max_tokens=max_tokens,
                n=n,
                tools=adapted_inputs.tools,
            )

            return MistralChatResponseAdapter(response)

        elif self.provider == "anthropic":
            if n != 1:
                warnings.warn(f"Anthropic models ({self.model_name}) only support n=1. Ignoring n={n}.")

            if max_tokens is None:
                raise ValueError(f"max_tokens must be set for Anthropic models ({self.model_name}).")

            adapted_inputs = AnthropicChatInputsAdapter(messages, tools=tools)

            response = self.client.messages.create(
                model=self.model_name,
                messages=adapted_inputs.messages,
                system=adapted_inputs.system_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                tools=adapted_inputs.tools,
            )

            return AnthropicChatResponseAdapter(response)

        elif self.provider == "google":
            import google.generativeai as genai

            adapted_inputs = GoogleChatInputsAdapter(messages, tools)

            if self.client is None:
                self.client = genai.GenerativeModel(self.model_name, system_instruction=adapted_inputs.system_prompt)

            response = self.client.generate_content(
                contents=adapted_inputs.messages,
                generation_config=genai.types.GenerationConfig(
                    candidate_count=n,
                    max_output_tokens=max_tokens,
                    temperature=temperature,
                ),
                tools=adapted_inputs.tools,
            )

            return GoogleChatResponseAdapter(response)

    def embed(self, input: Union[str, List[str]]) -> TextEmbeddingResponse:
        """
        Embeds the input text using the AI model.

        Args:
            input (Union[str, List[str]]): The input text to embed. Can be a single string or a list of strings.

        Returns:
            EmbeddingResponse: The response from the model.
        """
        if self.model_category != "embed":
            raise ValueError(f"Model '{self.model_name}' is not an embedding model.")

        if self.provider == "openai":
            response = self.client.embeddings.create(input=input, model=self.model_name)

            return OpenAITextEmbeddingResponseAdapter(response)

        elif self.provider == "mistral":
            response = self.client.embeddings.create(
                model=self.model_name,
                inputs=input,
            )

            return MistralTextEmbeddingResponseAdapter(response)

        elif self.provider == "google":
            import google.generativeai as genai

            if isinstance(input, str):
                input = [input]

            response = genai.embed_content(
                content=input,
                model=self.model_name,
            )

            return GoogleTextEmbeddingResponseAdapter(response)

        elif self.provider == "voyageai":
            response = self.client.embed(input, model=self.model_name)

            return VoyageAITextEmbeddingResponseAdapter(response)

    def transcribe(self, audio_path: str, language: str = None) -> TranscriptionResponse:
        """
        Convert speech to text.

        Args:
            audio_path (str): The path to the audio file.
            language (str, optional): The language of the audio file.

        Returns:
            TranscriptionResponse: The response from the model.
        """

        if self.model_category != "transcribe":
            raise ValueError(f"Model '{self.model_name}' is not a speech-to-text model.")

        if self.provider == "openai":
            with open(audio_path, "rb") as audio_file:
                response = self.client.audio.transcriptions.create(
                    model=self.model_name, file=audio_file, language=language
                )

            return OpenAITranscriptionResponseAdapter(response)

        elif self.provider == "deepgram":
            from deepgram import PrerecordedOptions, FileSource

            with open(audio_path, "rb") as file:
                buffer_data = file.read()

            payload: FileSource = {
                "buffer": buffer_data,
            }

            options = PrerecordedOptions(
                model=self.model_name,
                language=language,
            )

            response = self.client.listen.rest.v("1").transcribe_file(payload, options)

            return DeepgramTranscriptionResponseAdapter(response)

    @staticmethod
    def get_model_category(model_name: str) -> str:
        """
        Returns the category of a model.

        Args:
            model_name: The name of the model.

        Returns:
            str: The category of the model.
        """
        for categories in SUPPORTED_MODELS.values():
            for category, model_list in categories.items():
                if model_name in model_list:
                    return category

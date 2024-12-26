from abc import ABC
from typing import Union, List, Optional

from switchai.types import (
    ChatResponse,
    TextEmbeddingResponse,
    TranscriptionResponse,
    ImageGenerationResponse,
    ChatChoice,
)


class BaseClient(ABC):
    def chat(
        self,
        messages: List[str | ChatChoice | dict],
        temperature: float = 1.0,
        max_tokens: Optional[int] = None,
        n: int = 1,
        tools: Optional[List] = None,
    ) -> ChatResponse:
        """
        Sends a chat request to the AI model and returns the response.

        Args:
            messages (List[str | ChatChoice | dict]): A list of messages to send to the model.
            temperature (float, optional): Sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. Defaults to 1.0.
            max_tokens (int, optional): The maximum number of tokens to generate. Defaults to None.
            n (int, optional): How many chat completion choices to generate for each input message. Defaults to 1.
            tools (List, optional): A list of tools the model may call. Defaults to None.

        Returns:
            ChatResponse: The response from the model.
        """
        pass

    def embed(self, inputs: Union[str, List[str]]) -> TextEmbeddingResponse:
        """
        Embeds the input text using the AI model.

        Args:
            inputs (Union[str, List[str]]): The input text to embed. Can be a single string or a list of strings.

        Returns:
            TextEmbeddingResponse: The response from the model.
        """
        pass

    def transcribe(self, audio_path: str, language: Optional[str] = None) -> TranscriptionResponse:
        """
        Convert speech to text.

        Args:
            audio_path (str): The path to the audio file.
            language (str, optional): The language of the audio file.

        Returns:
            TranscriptionResponse: The response from the model.
        """
        pass

    def generate_image(self, prompt: str, n: int = 1) -> ImageGenerationResponse:
        """
        Generate an image based on the provided prompt.

        Args:
            prompt (str): A text description of the desired image.
            n (int, optional): The number of images to generate. Defaults to 1.

        Returns:
            ImageGenerationResponse: The response from the model.
        """
        pass

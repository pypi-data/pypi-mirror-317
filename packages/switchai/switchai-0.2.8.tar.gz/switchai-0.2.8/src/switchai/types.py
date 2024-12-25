from typing import Dict, Any, List, Optional

from PIL.Image import Image
from pydantic import BaseModel, field_validator, ValidationError


class Function(BaseModel):
    """
    The function called by the model.

    Args:
        name (str): The name of the function.
        arguments (Dict[str, Any]): The arguments of the function.
    """

    name: str
    arguments: Dict[str, Any]


class ChatMessage(BaseModel):
    """
    The generated chat message.

    Args:
        role (str): The role of the author of this message.
        content (str | None): The content of the message.
    """

    role: str
    content: Optional[str] = None


class ChatToolCall(BaseModel):
    """
    A chat tool call.

    Args:
        id (str | None): A unique identifier of the tool call.
        function (:class:`~switchai.response.Function`): The function called.
        type (str): The function type. Always "function".
    """

    id: Optional[str] = None
    function: Function
    type: str = "function"


class ChatChoice(BaseModel):
    """
    A chat choice.

    Args:
        index (int): The index of the choice.
        message (:class:`~switchai.response.ChatMessage`): The generated message.
        finish_reason (str): The reason the generation finished.
        tool_calls (List[:class:`~switchai.response.ChatToolCall`] | None): A list of tool calls.
    """

    index: int
    message: ChatMessage
    finish_reason: str
    tool_calls: Optional[List[ChatToolCall]] = None


class ChatUsage(BaseModel):
    """
    Usage statistics for a chat response.

    Args:
        input_tokens (int): The number of input tokens used.
        output_tokens (int): The number of output tokens generated.
        total_tokens (int): The total number of tokens used.
    """

    input_tokens: int
    output_tokens: int
    total_tokens: int


class ChatResponse(BaseModel):
    """
    Represents a chat response from the model, based on the provided input.

    Args:
        id (str | None): A unique identifier of the response.
        object (str | None): The object type.
        model (str | None): The model used to generate the response.
        usage (:class:`~switchai.response.ChatUsage`): Usage statistics.
        choices (List[ChatChoice]): A list of choices. Can be more than 1 if `n` is greater than 1.
    """

    id: Optional[str] = None
    object: Optional[str] = None
    model: Optional[str] = None
    usage: ChatUsage
    choices: List[ChatChoice]


class Embedding(BaseModel):
    """
    An embedding vector representing the input text.

    Args:
        index (int): The index of the embedding in the list of embeddings.
        data (List[float]): The embedding vector, which is a list of floats.
    """

    index: int
    data: List[float]


class EmbeddingUsage(BaseModel):
    """
    Usage statistics for an embedding response.

    Args:
        input_tokens (int | None): The number of input tokens used.
        total_tokens (int | None): The total number of tokens used.
    """

    input_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


class TextEmbeddingResponse(BaseModel):
    """
    Represents an embedding response from the model, based on the provided input.

    Args:
        id (str | None): A unique identifier of the response.
        object (str | None): The object type.
        model (str | None): The model used to generate the response.
        usage (:class:`~switchai.response.EmbeddingUsage`): Usage statistics.
        embeddings (List[:class:`~switchai.response.Embedding`]): A list of embeddings.
    """

    id: Optional[str] = None
    object: Optional[str] = None
    model: Optional[str] = None
    usage: EmbeddingUsage
    embeddings: List[Embedding]


class TranscriptionResponse(BaseModel):
    """
    A transcription of an input audio.

    Args:
        text (str): The transcribed text.
    """

    text: str


class OpenAITranscriptionResponseAdapter(TranscriptionResponse):
    def __init__(self, response):
        super().__init__(text=response.text)


class DeepgramTranscriptionResponseAdapter(TranscriptionResponse):
    def __init__(self, response):
        super().__init__(text=response["results"]["channels"][0]["alternatives"][0]["transcript"])


class ImageGenerationResponse(BaseModel):
    """
    Represents an image generation response from the model, based on the provided input.

    Args:
        images (List[:class:`~PIL.Image.Image`]): A list of generated images.
    """

    images: List[Any]

    @field_validator("images", mode="before")
    def validate_images(cls, value):
        if isinstance(value, list):
            for img in value:
                if not isinstance(img, Image):
                    raise ValidationError("Each item must be a valid PIL.Image instance.")
            return value
        raise ValidationError("The value must be a list of PIL.Image instances.")

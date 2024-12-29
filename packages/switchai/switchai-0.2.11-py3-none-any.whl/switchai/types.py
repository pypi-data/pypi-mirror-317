from typing import Dict, Any, List, Optional

from PIL.Image import Image
from pydantic import BaseModel, field_validator, ValidationError


class Function(BaseModel):
    """
    The function called by the model.

    Args:
        name: The name of the function.
        arguments: The arguments of the function.
    """

    name: str
    arguments: Dict[str, Any]


class ChatMessage(BaseModel):
    """
    The generated chat message.

    Args:
        role: The role of the author of this message.
        content: The content of the message.
    """

    role: Optional[str] = None
    content: Optional[str] = None


class ChatToolCall(BaseModel):
    """
    A chat tool call.

    Args:
        id: A unique identifier of the tool call.
        function: The function called.
        type: The function type. Always "function".
    """

    id: Optional[str] = None
    function: Function
    type: str = "function"


class ChatChoice(BaseModel):
    """
    A chat choice.

    Args:
        index: The index of the choice.
        message: The generated message.
        finish_reason: The reason the generation finished.
        tool_calls: A list of tool calls.
    """

    index: int
    message: Optional[ChatMessage] = None
    finish_reason: Optional[str] = None
    tool_calls: Optional[List[ChatToolCall]] = None


class ChatUsage(BaseModel):
    """
    Usage statistics for a chat response.

    Args:
        input_tokens: The number of input tokens used.
        output_tokens: The number of output tokens generated.
        total_tokens: The total number of tokens used.
    """

    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


class ChatResponse(BaseModel):
    """
    Represents a chat response from the model, based on the provided input.

    Args:
        id: A unique identifier of the response.
        object: The object type.
        model: The model used to generate the response.
        usage: Usage statistics.
        choices: A list of choices. Can be more than 1 if `n` is greater than 1.
    """

    id: Optional[str] = None
    object: Optional[str] = None
    model: Optional[str] = None
    usage: Optional[ChatUsage] = None
    choices: List[ChatChoice]


class Embedding(BaseModel):
    """
    An embedding vector representing the input text.

    Args:
        index: The index of the embedding in the list of embeddings.
        data: The embedding vector, which is a list of floats.
    """

    index: int
    data: List[float]


class EmbeddingUsage(BaseModel):
    """
    Usage statistics for an embedding response.

    Args:
        input_tokens: The number of input tokens used.
        total_tokens: The total number of tokens used.
    """

    input_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


class EmbeddingResponse(BaseModel):
    """
    Represents an embedding response from the model, based on the provided input.

    Args:
        id: A unique identifier of the response.
        object: The object type.
        model: The model used to generate the response.
        usage: Usage statistics.
        embeddings: A list of embeddings.
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
        text: The transcribed text.
    """

    text: str


class ImageGenerationResponse(BaseModel):
    """
    Represents an image generation response from the model, based on the provided input.

    Args:
        images: A list of generated images.
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

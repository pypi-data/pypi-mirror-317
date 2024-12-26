import copy
import json
from typing import Union, List, Optional

from ..base_client import BaseClient
from ..types import (
    ChatChoice,
    ChatResponse,
    ChatUsage,
    ChatMessage,
    ChatToolCall,
    Function,
    TextEmbeddingResponse,
    EmbeddingUsage,
    Embedding,
)
from ..utils import encode_image, is_url
from mistralai import Mistral


class MistralClientAdapter(BaseClient):
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.client = Mistral(api_key=api_key)

    def chat(
        self,
        messages: List[str],
        temperature: float = 1.0,
        max_tokens: Optional[int] = None,
        n: int = 1,
        tools: Optional[List] = None,
    ) -> ChatResponse:
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

    def embed(self, inputs: Union[str, List[str]]) -> TextEmbeddingResponse:
        response = self.client.embeddings.create(
            model=self.model_name,
            inputs=inputs,
        )

        return MistralTextEmbeddingResponseAdapter(response)


class MistralChatInputsAdapter:
    def __init__(self, messages, tools=None):
        self.messages = [self._adapt_message(m) for m in messages]
        self.tools = tools

    def _adapt_message(self, message):
        if isinstance(message, ChatChoice):
            return self._adapt_chat_choice(message)

        if message["role"] == "tool":
            return self._adapt_tool_message(message)

        if message["role"] == "user":
            return self._adapt_user_message(message)

        return message

    def _adapt_chat_choice(self, chat_choice):
        adapted_message = {
            "role": chat_choice.message.role,
            "content": chat_choice.message.content,
        }
        if chat_choice.tool_calls:
            adapted_message["tool_calls"] = [tool_call.dict() for tool_call in chat_choice.tool_calls]

        return adapted_message

    def _adapt_tool_message(self, message):
        adapted_tool_message = copy.deepcopy(message)
        adapted_tool_message["name"] = adapted_tool_message.pop("tool_name")

        return adapted_tool_message

    def _adapt_user_message(self, message):
        original_content = message.get("content", [])
        adapted_content = []

        if isinstance(original_content, list):
            for content_item in original_content:
                adapted_content.append(self._adapt_content_item(content_item))
        elif isinstance(original_content, str):
            adapted_content.append({"type": "text", "text": original_content})

        return {"role": "user", "content": adapted_content}

    def _adapt_content_item(self, content_item):
        if content_item.get("type") == "text":
            return {"type": "text", "text": content_item["text"]}
        elif content_item.get("type") == "image":
            return self._adapt_image_content(content_item)
        return content_item

    def _adapt_image_content(self, content_item):
        image = content_item.get("image")
        if is_url(image):
            return {"type": "image_url", "image_url": {"url": image}}
        base64_image = encode_image(image)
        return {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}


class MistralChatResponseAdapter(ChatResponse):
    def __init__(self, response):
        super().__init__(
            id=response.id,
            object=response.object,
            model=response.model,
            usage=ChatUsage(
                input_tokens=response.usage.prompt_tokens,
                output_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
            ),
            choices=[
                ChatChoice(
                    index=choice.index,
                    message=ChatMessage(role=choice.message.role, content=choice.message.content),
                    tool_calls=[
                        ChatToolCall(
                            id=tool.id,
                            function=Function(name=tool.function.name, arguments=json.loads(tool.function.arguments)),
                        )
                        for tool in choice.message.tool_calls
                    ]
                    if choice.message.tool_calls is not None
                    else None,
                    finish_reason=choice.finish_reason,
                )
                for choice in response.choices
            ],
        )


class MistralTextEmbeddingResponseAdapter(TextEmbeddingResponse):
    def __init__(self, response):
        super().__init__(
            id=response.id,
            object=response.object,
            model=response.model,
            usage=EmbeddingUsage(
                input_tokens=response.usage.prompt_tokens,
                total_tokens=response.usage.total_tokens,
            ),
            embeddings=[
                Embedding(
                    index=embedding.index,
                    data=embedding.embedding,
                )
                for embedding in response.data
            ],
        )

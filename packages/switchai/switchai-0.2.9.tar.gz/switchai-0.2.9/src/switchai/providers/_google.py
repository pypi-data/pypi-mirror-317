from typing import Union, List, Optional

import google.generativeai as genai
import httpx

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
from ..utils import is_url, encode_image


class GoogleClientAdapter(BaseClient):
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        # Delay the client creation until the chat method is called
        # because a system prompt can't be set after the client is created
        self.client = None

        genai.configure(api_key=api_key)

    def chat(
        self,
        messages: List[str],
        temperature: float = 1.0,
        max_tokens: Optional[int] = None,
        n: int = 1,
        tools: Optional[List] = None,
    ) -> ChatResponse:
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

    def embed(self, inputs: Union[str, List[str]]) -> TextEmbeddingResponse:
        if isinstance(inputs, str):
            inputs = [inputs]

        response = genai.embed_content(
            content=inputs,
            model=self.model_name,
        )

        return GoogleTextEmbeddingResponseAdapter(response)


class GoogleChatInputsAdapter:
    def __init__(self, messages, tools=None):
        self.system_prompt = None
        if messages[0]["role"] == "system":
            self.system_prompt = messages[0]["content"]
            messages = messages[1:]

        self.messages = [self._adapt_message(m) for m in messages]
        self.tools = self._adapt_tools(tools)

    def _adapt_message(self, message):
        if isinstance(message, ChatChoice):
            return self._adapt_chat_choice(message)
        if message["role"] == "tool":
            return self._adapt_tool_message(message)
        if message["role"] == "user":
            return self._adapt_user_message(message)

        return {"role": message["role"], "parts": message["content"]}

    def _adapt_chat_choice(self, chat_choice):
        if chat_choice.tool_calls:
            return {
                "role": chat_choice.message.role,
                "parts": [
                    {
                        "function_call": {
                            "name": chat_choice.tool_calls[0].function.name,
                            "args": chat_choice.tool_calls[0].function.arguments,
                        }
                    }
                ],
            }
        return {"role": chat_choice.message.role, "parts": chat_choice.message.content}

    def _adapt_tool_message(self, message):
        return {
            "role": "user",
            "parts": [
                {
                    "function_response": {
                        "name": message["tool_name"],
                        "response": {
                            "name": message["tool_name"],
                            "content": message["content"],
                        },
                    }
                }
            ],
        }

    def _adapt_user_message(self, message):
        original_content = message.get("content", [])
        adapted_content = []

        if isinstance(original_content, list):
            for content_item in original_content:
                adapted_content.append(self._adapt_content_item(content_item))
        elif isinstance(original_content, str):
            adapted_content.append({"text": original_content})

        return {"role": message["role"], "parts": adapted_content}

    def _adapt_content_item(self, content_item):
        if content_item.get("type") == "text":
            return {"text": content_item["text"]}
        elif content_item.get("type") == "image":
            return self._adapt_image_content(content_item)

        return content_item

    def _adapt_image_content(self, content_item):
        image = content_item.get("image")
        if is_url(image):
            image = httpx.get(image).content
        base64_image = encode_image(image)
        return {"mime_type": "image/jpeg", "data": base64_image}

    def _adapt_tools(self, tools):
        adapted_tools = None

        if tools:
            adapted_tools = [{"function_declarations": []}]
            for tool in tools:
                function = tool["function"]
                if "description" not in function:
                    function["description"] = ""
                adapted_tools[0]["function_declarations"].append(function)

        return adapted_tools


class GoogleChatResponseAdapter(ChatResponse):
    def __init__(self, response):
        super().__init__(
            id=None,
            object=None,
            model=None,
            usage=ChatUsage(
                input_tokens=response.usage_metadata.prompt_token_count,
                output_tokens=response.usage_metadata.candidates_token_count,
                total_tokens=response.usage_metadata.total_token_count,
            ),
            choices=[
                ChatChoice(
                    index=choice.index,
                    message=ChatMessage(role="assistant", content=choice.content.parts[0].text),
                    tool_calls=[
                        ChatToolCall(
                            id=None,
                            function=Function(name=part.function_call.name, arguments=dict(part.function_call.args)),
                        )
                        for part in choice.content.parts
                        if "function_call" in part
                    ],
                    finish_reason=choice.finish_reason.name.lower(),
                )
                for choice in response.candidates
            ],
        )


class GoogleTextEmbeddingResponseAdapter(TextEmbeddingResponse):
    def __init__(self, response):
        super().__init__(
            id=None,
            object=None,
            model=None,
            usage=EmbeddingUsage(
                input_tokens=None,
                total_tokens=None,
            ),
            embeddings=[
                Embedding(
                    index=index,
                    data=data,
                )
                for index, data in enumerate(response["embedding"])
            ],
        )

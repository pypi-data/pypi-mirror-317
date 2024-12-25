import copy

from anthropic import NOT_GIVEN

from ..types import ChatChoice, ChatResponse, ChatUsage, ChatMessage, ChatToolCall, Function
from ..utils import is_url, encode_image


class AnthropicChatInputsAdapter:
    def __init__(self, messages, tools=None):
        self.system_prompt = NOT_GIVEN
        if messages and messages[0].get("role") == "system":
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

        return message

    def _adapt_chat_choice(self, chat_choice):
        if chat_choice.tool_calls:
            return {
                "role": chat_choice.message.role,
                "content": [
                    {"type": "text", "text": chat_choice.message.content},
                    {
                        "type": "tool_use",
                        "id": chat_choice.tool_calls[0].id,
                        "name": chat_choice.tool_calls[0].function.name,
                        "input": chat_choice.tool_calls[0].function.arguments,
                    },
                ],
            }
        return {"role": chat_choice.message.role, "content": chat_choice.message.content}

    def _adapt_tool_message(self, message):
        return {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": message["tool_call_id"],
                    "content": message["content"],
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
            adapted_content.append({"type": "text", "text": original_content})

        return {"role": message["role"], "content": adapted_content}

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
        return {
            "type": "image",
            "source": {"type": "base64", "media_type": "image/jpeg", "data": base64_image},
        }

    def _adapt_tools(self, tools):
        if not tools:
            return []

        adapted_tools = []
        for tool in tools:
            tool_copy = copy.deepcopy(tool)
            tool_copy["function"]["input_schema"] = tool_copy["function"].pop("parameters")
            adapted_tools.append(tool_copy["function"])

        return adapted_tools


class AnthropicChatResponseAdapter(ChatResponse):
    def __init__(self, response):
        super().__init__(
            id=response.id,
            object=None,
            model=response.model,
            usage=ChatUsage(
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens,
                total_tokens=response.usage.input_tokens + response.usage.output_tokens,
            ),
            choices=[
                ChatChoice(
                    index=0,
                    message=ChatMessage(role=response.role, content=response.content[0].text),
                    tool_calls=[
                        ChatToolCall(
                            id=response.content[1].id,
                            function=Function(name=response.content[1].name, arguments=response.content[1].input),
                        )
                    ]
                    if len(response.content) > 1
                    else None,
                    finish_reason=response.stop_reason,
                )
            ],
        )

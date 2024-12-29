from openai import OpenAI

from ._openai import OpenaiClientAdapter


SUPPORTED_MODELS = {"chat": ["grok-beta", "grok-vision-beta"]}

API_KEY_NAMING = "XAI_API_KEY"


class XaiClientAdapter(OpenaiClientAdapter):
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")

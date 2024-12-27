from openai import OpenAI

from ._openai import OpenaiClientAdapter


class XaiClientAdapter(OpenaiClientAdapter):
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")

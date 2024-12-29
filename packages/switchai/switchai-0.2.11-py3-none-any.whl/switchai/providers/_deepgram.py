from typing import Optional

from deepgram import DeepgramClient, PrerecordedOptions, FileSource

from ..base_client import BaseClient
from ..types import TranscriptionResponse


SUPPORTED_MODELS = {
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
}

API_KEY_NAMING = "DEEPGRAM_API_KEY"


class DeepgramClientAdapter(BaseClient):
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.client = DeepgramClient(api_key=api_key)

    def transcribe(self, audio_path: str, language: Optional[str] = None) -> TranscriptionResponse:
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


class DeepgramTranscriptionResponseAdapter(TranscriptionResponse):
    def __init__(self, response):
        super().__init__(text=response["results"]["channels"][0]["alternatives"][0]["transcript"])

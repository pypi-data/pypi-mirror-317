from ..types import TranscriptionResponse


class DeepgramTranscriptionResponseAdapter(TranscriptionResponse):
    def __init__(self, response):
        super().__init__(text=response["results"]["channels"][0]["alternatives"][0]["transcript"])

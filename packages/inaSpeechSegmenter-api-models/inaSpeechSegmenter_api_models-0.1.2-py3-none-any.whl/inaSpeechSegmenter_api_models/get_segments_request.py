from inaSpeechSegmenter_api_models.request_base import SegmenterRequestBase

class GetSegmentsRequest(SegmenterRequestBase):
    filename: str
    audio_bytes_base64: str

    @classmethod
    def get_endpoint(cls) -> str:
        return "get_segments"

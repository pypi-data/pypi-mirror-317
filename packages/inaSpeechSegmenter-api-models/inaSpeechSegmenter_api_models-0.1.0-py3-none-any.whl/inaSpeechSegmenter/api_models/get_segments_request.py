from pydantic import BaseModel

class GetSegmentsRequest(BaseModel):
    filename: str
    audio_bytes_base64: str

from pydantic import BaseModel

class SegmenterRequestBase(BaseModel):
    @classmethod
    def get_endpoint(cls) -> str:
        raise NotImplementedError()

from pydantic import BaseModel

class SegmentItem(BaseModel):
    label: str
    start_time: float
    end_time: float

from inaSpeechSegmenter.api_models.segment_item import SegmentItem

from typing import List

from pydantic import BaseModel

class GetSegmentsResponse(BaseModel):
    segments: List[SegmentItem]

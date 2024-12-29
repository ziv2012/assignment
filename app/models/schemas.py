from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime

class DetectionRequest(BaseModel):
    prompt: str
    settings: Dict[str, bool]

class DetectionResponse(BaseModel):
    detected_topics: List[str]

class LogEntry(BaseModel):
    timestamp: datetime
    endpoint: str
    prompt: str
    settings: Dict[str, bool]
    result: List[str]
    processing_time: float
    is_successful: bool
    error_message: str
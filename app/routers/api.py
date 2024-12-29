from fastapi import APIRouter, HTTPException
from typing import Optional
import time

from app.models.schemas import DetectionRequest, DetectionResponse
from app.services.detector import TopicDetector
from app.services.logger import audit_logger

router = APIRouter()

@router.post("/detect", response_model=DetectionResponse)
async def detect_endpoint(request: DetectionRequest):
    start_time = time.time()
    
    if not request.prompt:
        audit_logger.log_request("/detect", request.prompt, request.settings, [], 0, False, "Prompt cannot be empty")
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    detected = await TopicDetector.detect_topics(request.prompt, request.settings, fast_mode=False)
    
    processing_time = time.time() - start_time
    audit_logger.log_request("/detect", request.prompt, request.settings, detected, processing_time, True, "")
    
    return DetectionResponse(detected_topics=detected)

@router.post("/protect", response_model=DetectionResponse)
async def protect_endpoint(request: DetectionRequest):
    start_time = time.time()
    
    if not request.prompt:
        audit_logger.log_request("/detect", request.prompt, request.settings, [], 0, False, "Prompt cannot be empty")
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    detected = await TopicDetector.detect_topics(request.prompt, request.settings, fast_mode=True)
    
    processing_time = time.time() - start_time
    audit_logger.log_request("/protect", request.prompt, request.settings, detected, processing_time, True, "")
    
    return DetectionResponse(detected_topics=detected)

@router.get("/logs")
async def get_logs(limit: Optional[int] = 100):
    """Return the most recent logs, limited by the specified number"""
    return audit_logger.get_recent_logs(limit)
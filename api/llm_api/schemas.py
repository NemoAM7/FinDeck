from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LLMPromptRequest(BaseModel):
    """Request model for LLM prompt API."""
    prompt: str
    model_name: Optional[str] = "llama-3.2-90b-vision-preview"  # Default model

class LLMPromptResponse(BaseModel):
    """Response model for LLM prompt API."""
    id: int
    prompt: str
    response: str
    prompt_type: str
    timestamp: datetime
    image_filename: Optional[str] = None
    model_used: Optional[str] = None
    processing_time: Optional[int] = None

    class Config:
        orm_mode = True

class LLMHistoryResponse(BaseModel):
    """Response model for retrieving LLM interaction history."""
    id: int
    prompt: str
    response: str
    prompt_type: str
    timestamp: datetime
    image_filename: Optional[str] = None
    
    class Config:
        orm_mode = True

class LLMImageResponse(BaseModel):
    """Response model for retrieving an image from an LLM interaction."""
    image_data: bytes
    image_filename: str 
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import Response
from typing import List, Dict, Optional
import io
import os
import time
from datetime import datetime
from sqlalchemy.orm import Session
from ..groq_client import GroqClient
from .models import LLMInteraction
from .schemas import LLMPromptRequest, LLMPromptResponse, LLMHistoryResponse, LLMImageResponse
from ..input_api.models import SessionLocal

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/prompt/text", response_model=LLMPromptResponse)
async def process_text_prompt(
    prompt_request: LLMPromptRequest,
    db: Session = Depends(get_db)
):
    """Process a text-only prompt."""
    # Initialize the Groq client
    groq_client = GroqClient(model_name=prompt_request.model_name)
    
    # Process the prompt
    result = await groq_client.process_text_prompt(
        prompt=prompt_request.prompt,
        model_name=prompt_request.model_name
    )
    
    # Create a database record
    llm_interaction = LLMInteraction(
        prompt=prompt_request.prompt,
        response=result["response"],
        prompt_type="text_only",
        model_used=result["model_used"],
        processing_time=result["processing_time"],
        timestamp=datetime.utcnow()
    )
    
    # Add to database
    db.add(llm_interaction)
    db.commit()
    db.refresh(llm_interaction)
    
    return llm_interaction

@router.post("/prompt/image", response_model=LLMPromptResponse)
async def process_image_prompt(
    prompt: str = Form(...),
    image: UploadFile = File(...),
    model_name: Optional[str] = Form("llama-3.2-90b-vision-preview"),
    db: Session = Depends(get_db)
):
    """Process a prompt with an image."""
    try:
        # Read image data
        start_time = time.time()
        image_data = await image.read()
        
        # Initialize the Groq client
        groq_client = GroqClient(model_name=model_name)
        
        # Process the multimodal prompt
        result = await groq_client.process_multimodal_prompt(
            text_prompt=prompt,
            image_bytes=image_data,
            model_name=model_name
        )
        
        # Create a database record with the image data
        llm_interaction = LLMInteraction(
            prompt=prompt,
            response=result["response"],
            prompt_type="text_and_image",
            image_data=image_data,
            image_filename=image.filename,
            model_used=result["model_used"],
            processing_time=result["processing_time"],
            timestamp=datetime.utcnow()
        )
        
        # Add to database
        db.add(llm_interaction)
        db.commit()
        db.refresh(llm_interaction)
        
        return llm_interaction
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image prompt: {str(e)}")

@router.post("/prompt/image-only", response_model=LLMPromptResponse)
async def process_image_only(
    image: UploadFile = File(...),
    model_name: Optional[str] = Form("llama-3.2-90b-vision-preview"),
    db: Session = Depends(get_db)
):
    """Process an image without a text prompt."""
    try:
        # Read image data
        image_data = await image.read()
        
        # Default prompt for image-only requests
        default_prompt = "What can you see in this image? Provide a detailed description."
        
        # Initialize the Groq client
        groq_client = GroqClient(model_name=model_name)
        
        # Process the multimodal prompt using the default prompt
        result = await groq_client.process_multimodal_prompt(
            text_prompt=default_prompt,
            image_bytes=image_data,
            model_name=model_name
        )
        
        # Create a database record with the image data
        llm_interaction = LLMInteraction(
            prompt=default_prompt,
            response=result["response"],
            prompt_type="image_only",
            image_data=image_data,
            image_filename=image.filename,
            model_used=result["model_used"],
            processing_time=result["processing_time"],
            timestamp=datetime.utcnow()
        )
        
        # Add to database
        db.add(llm_interaction)
        db.commit()
        db.refresh(llm_interaction)
        
        return llm_interaction
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@router.get("/history", response_model=List[LLMHistoryResponse])
async def get_interaction_history(db: Session = Depends(get_db)):
    """Get the history of LLM interactions."""
    try:
        # Query the database for all interactions, most recent first
        interactions = db.query(LLMInteraction).order_by(LLMInteraction.timestamp.desc()).all()
        return interactions
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving history: {str(e)}")

@router.get("/history/{interaction_id}", response_model=LLMPromptResponse)
async def get_interaction_detail(interaction_id: int, db: Session = Depends(get_db)):
    """Get details of a specific LLM interaction."""
    try:
        # Query the database for the specific interaction
        interaction = db.query(LLMInteraction).filter(LLMInteraction.id == interaction_id).first()
        
        if not interaction:
            raise HTTPException(status_code=404, detail="Interaction not found")
            
        return interaction
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving interaction: {str(e)}")

@router.get("/history/{interaction_id}/image")
async def get_interaction_image(interaction_id: int, db: Session = Depends(get_db)):
    """Get the image associated with a specific LLM interaction."""
    try:
        # Query the database for the specific interaction
        interaction = db.query(LLMInteraction).filter(LLMInteraction.id == interaction_id).first()
        
        if not interaction:
            raise HTTPException(status_code=404, detail="Interaction not found")
            
        if not interaction.image_data:
            raise HTTPException(status_code=404, detail="No image associated with this interaction")
            
        # Determine content type based on filename extension
        content_type = "image/jpeg"  # Default
        if interaction.image_filename:
            if interaction.image_filename.endswith(".png"):
                content_type = "image/png"
            elif interaction.image_filename.endswith(".gif"):
                content_type = "image/gif"
            elif interaction.image_filename.endswith(".webp"):
                content_type = "image/webp"
        
        # Return the image data directly
        return Response(content=interaction.image_data, media_type=content_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving image: {str(e)}") 
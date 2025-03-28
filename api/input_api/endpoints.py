from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from typing import List, Dict, Optional
import io
import csv
import os
from .schemas import CSVInput, CSVResponse
from sqlalchemy.orm import Session
from ..groq_client import GroqClient  # Use relative import

router = APIRouter()

# Check if running on Vercel

# In-memory storage for Vercel deployment
from .models import CSVData, SessionLocal, init_db
# Initialize the database when not on Vercel
init_db()

# Dependency to get the database session or in-memory store
def get_db():

    # Use SQLite for local development
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload-csv/", response_model=CSVResponse)
async def upload_csv(file: UploadFile = File(...), db: Optional[Session] = Depends(get_db)):
    """Upload a CSV file and store its content."""
    global next_id
    
    # Read CSV content from the uploaded file
    contents = await file.read()
    try:
        # Try to decode as text
        csv_content = contents.decode('utf-8')
        
        # Validate that it's a proper CSV
        csv_reader = csv.reader(io.StringIO(csv_content))
        list(csv_reader)  # Attempt to read the CSV to validate format
        
        
        csv_data = CSVData(
            filename=file.filename,
            content=csv_content,
            source_type="direct_upload"
        )
        db.add(csv_data)
        db.commit()
        db.refresh(csv_data)
        
        return {
            "id": csv_data.id,
            "filename": csv_data.filename,
            "source_type": csv_data.source_type
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid CSV file: {str(e)}")

@router.post("/upload-image/", response_model=CSVResponse)
async def upload_image(image: UploadFile = File(...), db: Optional[Session] = Depends(get_db)):
    """Process an image and extract CSV data."""
    global next_id
    
    try:
        # Read image data without saving to disk
        image_data = await image.read()
        
        # Process image using Groq client
        groq_client = GroqClient()
        csv_data_content = await groq_client.process_image_bytes(image_data)
        
        if not csv_data_content:
            raise HTTPException(
                status_code=400, 
                detail="Failed to extract CSV data from the image"
            )
        
    
        # Store CSV content in database for local development
        csv_data = CSVData(
            filename=f"{image.filename}_extracted.csv",
            content=csv_data_content,
            source_type="image_conversion"
        )
        db.add(csv_data)
        db.commit()
        db.refresh(csv_data)
        
        return {
            "id": csv_data.id,
            "filename": csv_data.filename,
            "source_type": csv_data.source_type
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing image: {str(e)}"
        )

@router.get("/csv/{csv_id}", response_model=CSVResponse)
def get_csv_info(csv_id: int, db: Optional[Session] = Depends(get_db)):
    """Get information about a stored CSV file."""
    

    csv_data = db.query(CSVData).filter(CSVData.id == csv_id).first()
    if not csv_data:
        raise HTTPException(status_code=404, detail="CSV data not found")
    
    return {
        "id": csv_data.id,
        "filename": csv_data.filename,
        "source_type": csv_data.source_type
    }

@router.get("/csv/{csv_id}/content")
def get_csv_content(csv_id: int, db: Optional[Session] = Depends(get_db)):
    """Get the content of a stored CSV file."""
    

    csv_data = db.query(CSVData).filter(CSVData.id == csv_id).first()
    if not csv_data:
        raise HTTPException(status_code=404, detail="CSV data not found")
    
    return {"content": csv_data.content}

@router.get("/csv/", response_model=List[CSVResponse])
def list_all_csvs(db: Optional[Session] = Depends(get_db)):
    """List all stored CSV files."""
    

    csv_data = db.query(CSVData).all()
    return [
        {"id": data.id, "filename": data.filename, "source_type": data.source_type}
        for data in csv_data
    ] 
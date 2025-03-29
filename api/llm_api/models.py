from sqlalchemy import Column, Integer, String, Text, DateTime, LargeBinary, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime
from ..input_api.models import Base, engine, SessionLocal

class LLMInteraction(Base):
    """Model to store LLM prompts and responses."""
    __tablename__ = 'llm_interactions'

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text, nullable=False)  # The text prompt sent to the LLM
    response = Column(Text, nullable=False)  # The response from the LLM
    prompt_type = Column(String, nullable=False)  # 'text_only', 'image_only', or 'text_and_image'
    image_data = Column(LargeBinary, nullable=True)  # Image data stored directly in the database
    image_filename = Column(String, nullable=True)  # Original filename of the image if provided
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Optional fields for additional metadata
    model_used = Column(String, nullable=True)  # The model name/version used
    processing_time = Column(Integer, nullable=True)  # Time taken to process in milliseconds

# Initialize database tables
def init_llm_db():
    """Create the LLM interaction table in the database."""
    Base.metadata.create_all(bind=engine) 
from pydantic import BaseModel
from typing import Optional

class CSVInput(BaseModel):
    filename: str
    content: str

class CSVResponse(BaseModel):
    id: int
    filename: str
    source_type: str

    class Config:
        orm_mode = True

class ImageInput(BaseModel):
    image_path: str  # Path to the image file 
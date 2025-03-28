from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def root():
    return {"message": "Welcome to the API! The server is running."}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

# Import the router only after the app is initialized
# Do not initialize database here to avoid size issues
from api.input_api.endpoints import router as input_api_router
app.include_router(input_api_router, prefix="/api/input", tags=["input"]) 
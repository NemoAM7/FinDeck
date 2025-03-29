from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.on_event("startup")
async def startup_event():
    """Initialize databases on startup"""
    # Initialize databases
    from api.input_api.models import init_db
    init_db()
    
    from api.llm_api.models import init_llm_db
    init_llm_db()

@app.get("/")
async def root():
    return {"message": "Welcome to the API! The server is running."}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

# Initialize databases
from api.input_api.models import init_db
init_db()

from api.llm_api.models import init_llm_db
init_llm_db()

# Include routers
from api.input_api.endpoints import router as input_api_router
app.include_router(input_api_router, prefix="/api/input", tags=["input"])

from api.llm_api.endpoints import router as llm_api_router
app.include_router(llm_api_router, prefix="/api/llm", tags=["llm"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 
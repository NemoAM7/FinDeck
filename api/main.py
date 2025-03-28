from fastapi import FastAPI
from api.input_api.endpoints import router as input_api_router
from api.input_api.models import init_db

app = FastAPI()

# Initialize the database
init_db()

app.include_router(input_api_router, prefix="/api/input", tags=["input"])
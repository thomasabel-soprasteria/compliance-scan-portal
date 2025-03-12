
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import os
from dotenv import load_dotenv

from app.api.routes import router as api_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.db.session import create_db_and_tables

# Load environment variables
load_dotenv()

# Configure logging
configure_logging()

app = FastAPI(
    title=settings.APP_NAME,
    description="API for analyzing annual reports for regulatory compliance",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create upload directory if it doesn't exist
os.makedirs(settings.TEMP_UPLOAD_DIR, exist_ok=True)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up compliance scan API")
    await create_db_and_tables()

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down compliance scan API")

# Include API routes
app.include_router(api_router, prefix=settings.API_PREFIX)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

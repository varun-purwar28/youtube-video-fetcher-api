from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from .database import engine, Base
from .api.videos import router as videos_router
from .tasks.background_tasks import BackgroundVideoFetcher
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="YouTube Video Fetcher API",
    description="A scalable API to fetch and store latest YouTube videos",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(videos_router)

# Initialize background task fetcher
background_fetcher = BackgroundVideoFetcher()

@app.on_event("startup")
async def startup_event():
    """Start background tasks on application startup"""
    background_fetcher.start()

@app.on_event("shutdown")
async def shutdown_event():
    """Stop background tasks on application shutdown"""
    background_fetcher.stop()

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "YouTube Video Fetcher API is running",
        "docs": "/docs",
        "api": "/api/v1/videos"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": str(logging.Formatter().formatTime(logging.LogRecord("test", logging.INFO, "", 0, "", (), None)))}

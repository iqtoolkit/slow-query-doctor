from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import analyze, config
from app.core.config import settings
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PostgreSQL Query Analyzer API",
    description="AI-powered PostgreSQL slow query analyzer using local Ollama (v0.2.0)",
    version="0.2.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analyze.router)
app.include_router(config.router)

@app.get("/")
async def root():
    return {
        "name": "PostgreSQL Query Analyzer API",
        "version": "0.2.0",
        "features": [
            "Single query analysis",
            "Local Ollama integration (privacy-focused)"
        ],
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
        workers=1  # Use 1 for development
    )
# backend/main.py
"""FastAPI application entry point."""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import sys
from pathlib import Path
import os

# Ensure the project root is in the path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from backend.config import settings
from backend.database.connection import init_db
from backend.api.routes import users, plans, progress, rag, health
from backend.core.middleware import ErrorHandlingMiddleware, RequestLoggingMiddleware

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("🚀 Starting Fitness & Diet Planner API...")
    
    try:
        init_db()
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("👋 Shutting down...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    ## RAG-powered AI Fitness & Diet Planner API
    
    This API provides personalized workout and diet plans using Retrieval-Augmented Generation.
    
    ### Features:
    - 🏋️ Personalized workout plans
    - 🥗 Customized diet plans (Indian veg/non-veg)
    - 📊 Progress tracking
    - 📈 Analytics and insights
    - 🤖 AI-powered recommendations
    
    ### RAG Architecture:
    The system uses verified fitness and nutrition data stored in a vector database
    to ground all AI-generated recommendations, preventing hallucination.
    """,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add middleware
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(ErrorHandlingMiddleware)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    health.router, 
    prefix=settings.API_PREFIX, 
    tags=["Health"]
)
app.include_router(
    users.router, 
    prefix=f"{settings.API_PREFIX}/users", 
    tags=["Users"]
)
app.include_router(
    plans.router, 
    prefix=f"{settings.API_PREFIX}/plans", 
    tags=["Plans"]
)
app.include_router(
    progress.router, 
    prefix=f"{settings.API_PREFIX}/progress", 
    tags=["Progress"]
)
app.include_router(
    rag.router, 
    prefix=f"{settings.API_PREFIX}/rag", 
    tags=["RAG"]
)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": f"{settings.API_PREFIX}/health"
    }


@app.get("/info", tags=["Root"])
async def info():
    """Get API information."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "debug": settings.DEBUG,
        "api_prefix": settings.API_PREFIX
    }

 # ✅ Always respect PORT env var from deployment platform
port = int(os.environ.get("PORT", settings.API_PORT))
host = "0.0.0.0"  # ✅ Force bind to all interfaces

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.app:app",
        host=host,
        port=port,
        reload=settings.DEBUG,
        log_level="debug" if settings.DEBUG else "info"
    )

# backend/api/routes/health.py
"""Health check endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.rag.vectorstore import get_pinecone_manager

router = APIRouter()


@router.get("/health")
async def health_check():
    """Basic health check."""
    return {"status": "healthy", "message": "API is running"}


@router.get("/health/db")
async def database_health(db: Session = Depends(get_db)):
    """Database health check."""
    try:
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}


@router.get("/health/vectorstore")
async def vectorstore_health():
    """Vector store health check."""
    try:
        pm = get_pinecone_manager()
        stats = pm.get_stats()
        return {
            "status": "healthy",
            "vectorstore": "connected",
            "stats": stats
        }
    except Exception as e:
        return {"status": "unhealthy", "vectorstore": str(e)}
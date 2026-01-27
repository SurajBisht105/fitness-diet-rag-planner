# backend/models/rag.py
"""RAG-related Pydantic models."""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime


class DocumentChunk(BaseModel):
    """Document chunk model for vector storage."""
    id: str
    content: str
    metadata: Dict
    embedding: Optional[List[float]] = None


class RetrievalQuery(BaseModel):
    """Query model for document retrieval."""
    query: str
    top_k: int = Field(default=5, ge=1, le=20)
    filter_type: Optional[str] = None  # "workout" or "diet"
    filter_level: Optional[str] = None  # "beginner", "intermediate", "advanced"


class RetrievedDocument(BaseModel):
    """Retrieved document model."""
    id: str
    content: str
    metadata: Dict
    score: float


class RAGQuery(BaseModel):
    """RAG query request model."""
    user_id: str
    query: str
    include_progress_context: bool = True
    plan_type: str = Field(..., pattern="^(workout|diet|both)$")


class RAGResponse(BaseModel):
    """RAG response model."""
    response: str
    sources: List[RetrievedDocument]
    confidence_score: float
    follow_up_questions: List[str]
    generated_at: datetime


class IngestionRequest(BaseModel):
    """Data ingestion request model."""
    documents: List[Dict]
    document_type: str  # "workout" or "diet"
    overwrite: bool = False


class IngestionResponse(BaseModel):
    """Data ingestion response model."""
    success: bool
    documents_processed: int
    chunks_created: int
    message: str
# backend/models/responses.py
"""Standard response models."""

from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, List, Any
from datetime import datetime

T = TypeVar('T')


class BaseResponse(BaseModel):
    """Base response model."""
    success: bool = True
    message: str = "Operation successful"
    timestamp: datetime = datetime.utcnow()


class DataResponse(BaseResponse, Generic[T]):
    """Response with data."""
    data: Optional[T] = None


class ListResponse(BaseResponse, Generic[T]):
    """Response with list of items."""
    data: List[T] = []
    total: int = 0
    page: int = 1
    page_size: int = 10


class ErrorResponse(BaseModel):
    """Error response model."""
    success: bool = False
    error: str
    message: str
    details: Optional[dict] = None
    timestamp: datetime = datetime.utcnow()


class PaginationParams(BaseModel):
    """Pagination parameters."""
    page: int = 1
    page_size: int = 10
    
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size
    
    @property
    def limit(self) -> int:
        return self.page_size


class HealthCheckResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    database: str
    vectorstore: str
    timestamp: datetime = datetime.utcnow()


class StatsResponse(BaseModel):
    """Statistics response."""
    total_users: int
    total_plans_generated: int
    total_workouts_logged: int
    total_calories_logged: int
    vectorstore_documents: int
# backend/core/exceptions.py
"""Custom exceptions for the application."""

from fastapi import HTTPException, status
from typing import Any, Optional, Dict


class FitnessPlannerException(Exception):
    """Base exception for Fitness Planner."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class UserNotFoundException(FitnessPlannerException):
    """Raised when a user is not found."""
    pass


class UserAlreadyExistsException(FitnessPlannerException):
    """Raised when trying to create a user that already exists."""
    pass


class PlanGenerationException(FitnessPlannerException):
    """Raised when plan generation fails."""
    pass


class RAGException(FitnessPlannerException):
    """Raised when RAG operations fail."""
    pass


class VectorStoreException(FitnessPlannerException):
    """Raised when vector store operations fail."""
    pass


class ValidationException(FitnessPlannerException):
    """Raised when validation fails."""
    pass


class DatabaseException(FitnessPlannerException):
    """Raised when database operations fail."""
    pass


# HTTP Exception factories
def not_found_exception(detail: str = "Resource not found") -> HTTPException:
    """Create a 404 Not Found exception."""
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


def bad_request_exception(detail: str = "Bad request") -> HTTPException:
    """Create a 400 Bad Request exception."""
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


def unauthorized_exception(detail: str = "Unauthorized") -> HTTPException:
    """Create a 401 Unauthorized exception."""
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def forbidden_exception(detail: str = "Forbidden") -> HTTPException:
    """Create a 403 Forbidden exception."""
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


def internal_server_error(detail: str = "Internal server error") -> HTTPException:
    """Create a 500 Internal Server Error exception."""
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=detail
    )
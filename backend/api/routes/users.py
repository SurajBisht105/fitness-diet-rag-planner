# backend/api/routes/users.py
"""User management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from backend.database.connection import get_db
from backend.models.user import (
    UserProfileCreate, UserProfileUpdate, 
    UserProfileResponse, UserStats
)
from backend.services.user_service import UserService

router = APIRouter()
user_service = UserService()


@router.post("/", response_model=UserProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserProfileCreate,
    db: Session = Depends(get_db)
):
    """Create a new user profile."""
    try:
        return user_service.create_user(db, user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=UserProfileResponse)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get user profile by ID."""
    user = user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/email/{email}", response_model=UserProfileResponse)
async def get_user_by_email(
    email: str,
    db: Session = Depends(get_db)
):
    """Get user profile by email."""
    user = user_service.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserProfileResponse)
async def update_user(
    user_id: str,
    user_data: UserProfileUpdate,
    db: Session = Depends(get_db)
):
    """Update user profile."""
    user = user_service.update_user(db, user_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Delete user profile."""
    if not user_service.delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/{user_id}/stats", response_model=UserStats)
async def get_user_stats(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get calculated stats for a user."""
    stats = user_service.get_user_stats(db, user_id)
    if not stats:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserStats(
        bmi=stats["bmi"],
        bmi_category=stats["bmi_category"],
        bmr=stats["bmr"],
        tdee=stats["tdee"],
        daily_calories=stats["daily_calories"],
        protein_g=stats["protein_g"],
        carbs_g=stats["carbs_g"],
        fats_g=stats["fats_g"]
    )
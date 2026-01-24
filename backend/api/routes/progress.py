# backend/api/routes/progress.py
"""Progress tracking endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional

from backend.database.connection import get_db
from backend.models.progress import (
    WeightLog, MeasurementLog, WorkoutLog, 
    CalorieLog, ProgressSummary, ProgressChartData
)
from backend.services.progress_service import ProgressService

router = APIRouter()
progress_service = ProgressService()


@router.post("/{user_id}/weight")
async def log_weight(
    user_id: str,
    weight_kg: float,
    log_date: Optional[date] = None,
    notes: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Log a weight entry."""
    if log_date is None:
        log_date = date.today()
    
    return progress_service.log_weight(db, user_id, weight_kg, log_date, notes)


@router.post("/{user_id}/measurements")
async def log_measurements(
    user_id: str,
    measurements: MeasurementLog,
    db: Session = Depends(get_db)
):
    """Log body measurements."""
    return progress_service.log_measurements(
        db, user_id, measurements.model_dump()
    )


@router.post("/{user_id}/workout")
async def log_workout(
    user_id: str,
    workout: WorkoutLog,
    db: Session = Depends(get_db)
):
    """Log workout completion."""
    return progress_service.log_workout(
        db, user_id, workout.model_dump()
    )


@router.post("/{user_id}/calories")
async def log_calories(
    user_id: str,
    calories: CalorieLog,
    db: Session = Depends(get_db)
):
    """Log daily calorie intake."""
    return progress_service.log_calories(
        db, user_id, calories.model_dump()
    )


@router.get("/{user_id}/summary", response_model=ProgressSummary)
async def get_progress_summary(
    user_id: str,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get progress summary."""
    return progress_service.get_progress_summary(db, user_id, days)


@router.get("/{user_id}/charts", response_model=ProgressChartData)
async def get_chart_data(
    user_id: str,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get data for progress charts."""
    return progress_service.get_chart_data(db, user_id, days)
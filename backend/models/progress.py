# backend/models/progress.py
"""Progress tracking Pydantic models."""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import date, datetime


class WeightLog(BaseModel):
    """Weight logging model."""
    weight_kg: float = Field(..., ge=30, le=300)
    date: date
    notes: Optional[str] = None


class MeasurementLog(BaseModel):
    """Body measurements model."""
    date: date
    chest_cm: Optional[float] = Field(None, ge=50, le=200)
    waist_cm: Optional[float] = Field(None, ge=40, le=200)
    hips_cm: Optional[float] = Field(None, ge=50, le=200)
    biceps_cm: Optional[float] = Field(None, ge=20, le=60)
    thighs_cm: Optional[float] = Field(None, ge=30, le=100)
    body_fat_percentage: Optional[float] = Field(None, ge=3, le=50)
    notes: Optional[str] = None


class WorkoutLog(BaseModel):
    """Workout completion log model."""
    date: date
    workout_day_id: str
    completed: bool
    exercises_completed: List[Dict]  # [{"exercise": "Bench Press", "sets": 3, "reps": [10, 8, 8], "weight_kg": 60}]
    duration_mins: int
    energy_level: int = Field(..., ge=1, le=10)
    notes: Optional[str] = None


class CalorieLog(BaseModel):
    """Daily calorie intake log model."""
    date: date
    meals: List[Dict]  # [{"meal": "Breakfast", "calories": 500, "items": ["Oats", "Banana"]}]
    total_calories: int
    total_protein: float
    total_carbs: float
    total_fats: float
    water_liters: float
    notes: Optional[str] = None


class ProgressSummary(BaseModel):
    """Progress summary model."""
    user_id: str
    period_start: date
    period_end: date
    
    # Weight progress
    starting_weight: float
    current_weight: float
    weight_change: float
    weight_trend: str  # "losing", "gaining", "maintaining"
    
    # Workout progress
    total_workouts_planned: int
    total_workouts_completed: int
    completion_rate: float
    
    # Calorie tracking
    avg_daily_calories: float
    calorie_target: int
    adherence_rate: float
    
    # Recommendations
    insights: List[str]
    adjustments_needed: List[str]


class ProgressChartData(BaseModel):
    """Data for progress charts."""
    weight_data: List[Dict]  # [{"date": "2024-01-01", "weight": 75.5}]
    calorie_data: List[Dict]  # [{"date": "2024-01-01", "intake": 2100, "target": 2000}]
    workout_data: List[Dict]  # [{"week": "Week 1", "completed": 4, "planned": 5}]
    measurement_data: List[Dict]
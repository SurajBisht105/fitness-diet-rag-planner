# backend/models/plan.py
"""Plan-related Pydantic models."""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import date
from enum import Enum


class MuscleGroup(str, Enum):
    CHEST = "chest"
    BACK = "back"
    SHOULDERS = "shoulders"
    BICEPS = "biceps"
    TRICEPS = "triceps"
    LEGS = "legs"
    CORE = "core"
    FULL_BODY = "full_body"


class Exercise(BaseModel):
    """Individual exercise model."""
    name: str
    muscle_group: MuscleGroup
    sets: int = Field(..., ge=1, le=10)
    reps: str  # Can be "8-12" or "30 sec"
    rest_seconds: int = Field(..., ge=0, le=300)
    notes: Optional[str] = None
    video_url: Optional[str] = None
    difficulty: str


class WorkoutDay(BaseModel):
    """Single workout day model."""
    day_name: str  # e.g., "Monday", "Day 1"
    focus: str  # e.g., "Push", "Legs", "Full Body"
    warm_up: List[str]
    exercises: List[Exercise]
    cool_down: List[str]
    estimated_duration_mins: int
    calories_burned_estimate: int


class WorkoutPlan(BaseModel):
    """Complete workout plan model."""
    id: str
    user_id: str
    plan_name: str
    description: str
    goal: str
    experience_level: str
    duration_weeks: int
    days_per_week: int
    schedule: List[WorkoutDay]
    progression_notes: str
    created_at: str
    sources: List[str]  # RAG sources used


class Meal(BaseModel):
    """Individual meal model."""
    name: str
    time: str  # e.g., "7:00 AM"
    items: List[str]
    calories: int
    protein_g: float
    carbs_g: float
    fats_g: float
    fiber_g: float
    recipe_notes: Optional[str] = None


class DailyDiet(BaseModel):
    """Single day diet plan model."""
    day_name: str
    total_calories: int
    total_protein: float
    total_carbs: float
    total_fats: float
    meals: List[Meal]
    water_intake_liters: float
    supplements: Optional[List[str]] = None


class DietPlan(BaseModel):
    """Complete diet plan model."""
    id: str
    user_id: str
    plan_name: str
    description: str
    dietary_preference: str
    daily_calorie_target: int
    macro_split: Dict[str, int]  # {"protein": 30, "carbs": 40, "fats": 30}
    schedule: List[DailyDiet]
    grocery_list: List[str]
    meal_prep_tips: List[str]
    created_at: str
    sources: List[str]  # RAG sources used


class PlanGenerationRequest(BaseModel):
    """Request model for plan generation."""
    user_id: str
    plan_type: str = Field(..., pattern="^(workout|diet|both)$")
    additional_preferences: Optional[str] = None
    exclude_exercises: Optional[List[str]] = None
    exclude_foods: Optional[List[str]] = None


class PlanGenerationResponse(BaseModel):
    """Response model for plan generation."""
    workout_plan: Optional[WorkoutPlan] = None
    diet_plan: Optional[DietPlan] = None
    recommendations: List[str]
    follow_up_questions: List[str]
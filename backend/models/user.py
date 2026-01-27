# backend/models/user.py
"""User-related Pydantic models for request/response validation."""

from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from datetime import datetime
from enum import Enum


class FitnessGoal(str, Enum):
    LEAN = "lean"
    MUSCLE_GAIN = "muscle_gain"
    FAT_LOSS = "fat_loss"


class ActivityLevel(str, Enum):
    SEDENTARY = "sedentary"
    LIGHTLY_ACTIVE = "lightly_active"
    MODERATELY_ACTIVE = "moderately_active"
    VERY_ACTIVE = "very_active"
    EXTREMELY_ACTIVE = "extremely_active"


class DietaryPreference(str, Enum):
    INDIAN_VEG = "indian_veg"
    INDIAN_NON_VEG = "indian_non_veg"
    VEGAN = "vegan"
    KETO = "keto"
    BALANCED = "balanced"


class ExperienceLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class WorkoutLocation(str, Enum):
    HOME = "home"
    GYM = "gym"
    BOTH = "both"


class UserProfileBase(BaseModel):
    """Base user profile model."""
    name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., ge=16, le=80)
    gender: Gender
    height_cm: float = Field(..., ge=100, le=250)
    weight_kg: float = Field(..., ge=30, le=300)
    fitness_goal: FitnessGoal
    activity_level: ActivityLevel
    dietary_preference: DietaryPreference
    experience_level: ExperienceLevel
    workout_location: WorkoutLocation
    workout_days_per_week: int = Field(..., ge=1, le=7)
    medical_conditions: Optional[str] = None
    allergies: Optional[str] = None


class UserProfileCreate(UserProfileBase):
    """Model for creating a new user profile."""
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    
    @validator('email')
    def email_to_lowercase(cls, v):
        return v.lower()


class UserProfileUpdate(BaseModel):
    """Model for updating user profile (all fields optional)."""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    age: Optional[int] = Field(None, ge=16, le=80)
    gender: Optional[Gender] = None
    height_cm: Optional[float] = Field(None, ge=100, le=250)
    weight_kg: Optional[float] = Field(None, ge=30, le=300)
    fitness_goal: Optional[FitnessGoal] = None
    activity_level: Optional[ActivityLevel] = None
    dietary_preference: Optional[DietaryPreference] = None
    experience_level: Optional[ExperienceLevel] = None
    workout_location: Optional[WorkoutLocation] = None
    workout_days_per_week: Optional[int] = Field(None, ge=1, le=7)
    medical_conditions: Optional[str] = None
    allergies: Optional[str] = None


class UserProfileResponse(UserProfileBase):
    """Model for user profile response."""
    id: str
    email: str
    created_at: datetime
    updated_at: datetime
    bmi: float
    bmr: float
    tdee: float
    
    class Config:
        from_attributes = True


class UserStats(BaseModel):
    """User statistics model."""
    bmi: float = Field(..., description="Body Mass Index")
    bmi_category: str
    bmr: float = Field(..., description="Basal Metabolic Rate")
    tdee: float = Field(..., description="Total Daily Energy Expenditure")
    daily_calories: int
    protein_g: int
    carbs_g: int
    fats_g: int
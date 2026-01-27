# backend/database/models.py
"""SQLAlchemy ORM models."""

from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from backend.database.connection import Base


def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    """User model."""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    height_cm = Column(Float, nullable=False)
    weight_kg = Column(Float, nullable=False)
    fitness_goal = Column(String, nullable=False)
    activity_level = Column(String, nullable=False)
    dietary_preference = Column(String, nullable=False)
    experience_level = Column(String, nullable=False)
    workout_location = Column(String, nullable=False)
    workout_days_per_week = Column(Integer, nullable=False)
    medical_conditions = Column(Text, nullable=True)
    allergies = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    weight_logs = relationship("WeightLog", back_populates="user", cascade="all, delete-orphan")
    measurement_logs = relationship("MeasurementLog", back_populates="user", cascade="all, delete-orphan")
    workout_logs = relationship("WorkoutLog", back_populates="user", cascade="all, delete-orphan")
    calorie_logs = relationship("CalorieLog", back_populates="user", cascade="all, delete-orphan")
    workout_plans = relationship("WorkoutPlanDB", back_populates="user", cascade="all, delete-orphan")
    diet_plans = relationship("DietPlanDB", back_populates="user", cascade="all, delete-orphan")


class WeightLog(Base):
    """Weight log model."""
    __tablename__ = "weight_logs"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    weight_kg = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="weight_logs")


class MeasurementLog(Base):
    """Body measurement log model."""
    __tablename__ = "measurement_logs"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    chest_cm = Column(Float, nullable=True)
    waist_cm = Column(Float, nullable=True)
    hips_cm = Column(Float, nullable=True)
    biceps_cm = Column(Float, nullable=True)
    thighs_cm = Column(Float, nullable=True)
    body_fat_percentage = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="measurement_logs")


class WorkoutLog(Base):
    """Workout completion log model."""
    __tablename__ = "workout_logs"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    workout_day_id = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    exercises_completed = Column(JSON, nullable=True)
    duration_mins = Column(Integer, nullable=True)
    energy_level = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="workout_logs")


class CalorieLog(Base):
    """Daily calorie intake log model."""
    __tablename__ = "calorie_logs"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    meals = Column(JSON, nullable=True)
    total_calories = Column(Integer, nullable=False)
    total_protein = Column(Float, nullable=True)
    total_carbs = Column(Float, nullable=True)
    total_fats = Column(Float, nullable=True)
    water_liters = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="calorie_logs")


class WorkoutPlanDB(Base):
    """Stored workout plan model."""
    __tablename__ = "workout_plans"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    plan_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    plan_data = Column(JSON, nullable=False)
    sources = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="workout_plans")


class DietPlanDB(Base):
    """Stored diet plan model."""
    __tablename__ = "diet_plans"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    plan_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    plan_data = Column(JSON, nullable=False)
    sources = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="diet_plans")
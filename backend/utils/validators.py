# backend/utils/validators.py
"""Input validation utilities."""

from typing import List, Optional
from pydantic import validator
import re


class InputValidator:
    """Collection of input validation methods."""
    
    @staticmethod
    def validate_age(age: int) -> bool:
        """Validate age is within acceptable range."""
        return 16 <= age <= 80
    
    @staticmethod
    def validate_height(height_cm: float) -> bool:
        """Validate height is within acceptable range."""
        return 100 <= height_cm <= 250
    
    @staticmethod
    def validate_weight(weight_kg: float) -> bool:
        """Validate weight is within acceptable range."""
        return 30 <= weight_kg <= 300
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_workout_days(days: int) -> bool:
        """Validate workout days per week."""
        return 1 <= days <= 7
    
    @staticmethod
    def sanitize_text(text: str) -> str:
        """Sanitize text input."""
        if not text:
            return ""
        # Remove potentially harmful characters
        sanitized = re.sub(r'[<>"\';{}]', '', text)
        return sanitized.strip()
    
    @staticmethod
    def validate_fitness_goal(goal: str) -> bool:
        """Validate fitness goal."""
        valid_goals = ["lean", "muscle_gain", "fat_loss"]
        return goal.lower() in valid_goals
    
    @staticmethod
    def validate_activity_level(level: str) -> bool:
        """Validate activity level."""
        valid_levels = [
            "sedentary", 
            "lightly_active", 
            "moderately_active", 
            "very_active", 
            "extremely_active"
        ]
        return level.lower() in valid_levels
    
    @staticmethod
    def validate_experience_level(level: str) -> bool:
        """Validate experience level."""
        valid_levels = ["beginner", "intermediate", "advanced"]
        return level.lower() in valid_levels
    
    @staticmethod
    def validate_dietary_preference(pref: str) -> bool:
        """Validate dietary preference."""
        valid_prefs = [
            "indian_veg", 
            "indian_non_veg", 
            "vegan", 
            "keto", 
            "balanced"
        ]
        return pref.lower() in valid_prefs
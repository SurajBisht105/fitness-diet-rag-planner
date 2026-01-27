# backend/services/user_service.py
"""User management service."""

from typing import Optional, Dict
from sqlalchemy.orm import Session

from backend.database.crud import UserCRUD
from backend.database.models import User
from backend.models.user import UserProfileCreate, UserProfileUpdate, UserProfileResponse
from backend.services.calorie_service import CalorieCalculator


class UserService:
    """Service for user-related operations."""
    
    def __init__(self):
        self.calorie_calculator = CalorieCalculator()
    
    def create_user(self, db: Session, user_data: UserProfileCreate) -> UserProfileResponse:
        """Create a new user with calculated stats."""
        # Check if user exists
        existing = UserCRUD.get_by_email(db, user_data.email)
        if existing:
            raise ValueError("User with this email already exists")
        
        # Create user
        user = UserCRUD.create(db, user_data)
        
        return self._user_to_response(user)
    
    def get_user(self, db: Session, user_id: str) -> Optional[UserProfileResponse]:
        """Get user by ID."""
        user = UserCRUD.get_by_id(db, user_id)
        if user:
            return self._user_to_response(user)
        return None
    
    def get_user_by_email(self, db: Session, email: str) -> Optional[UserProfileResponse]:
        """Get user by email."""
        user = UserCRUD.get_by_email(db, email)
        if user:
            return self._user_to_response(user)
        return None
    
    def update_user(self, db: Session, user_id: str, 
                    user_data: UserProfileUpdate) -> Optional[UserProfileResponse]:
        """Update user profile."""
        user = UserCRUD.update(db, user_id, user_data)
        if user:
            return self._user_to_response(user)
        return None
    
    def delete_user(self, db: Session, user_id: str) -> bool:
        """Delete user."""
        return UserCRUD.delete(db, user_id)
    
    def get_user_stats(self, db: Session, user_id: str) -> Optional[Dict]:
        """Get calculated stats for a user."""
        user = UserCRUD.get_by_id(db, user_id)
        if not user:
            return None
        
        profile = {
            "weight_kg": user.weight_kg,
            "height_cm": user.height_cm,
            "age": user.age,
            "gender": user.gender,
            "activity_level": user.activity_level,
            "fitness_goal": user.fitness_goal
        }
        
        return self.calorie_calculator.calculate_all(profile)
    
    def _user_to_response(self, user: User) -> UserProfileResponse:
        """Convert User model to response with calculated stats."""
        profile = {
            "weight_kg": user.weight_kg,
            "height_cm": user.height_cm,
            "age": user.age,
            "gender": user.gender,
            "activity_level": user.activity_level,
            "fitness_goal": user.fitness_goal
        }
        
        stats = self.calorie_calculator.calculate_all(profile)
        
        return UserProfileResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            age=user.age,
            gender=user.gender,
            height_cm=user.height_cm,
            weight_kg=user.weight_kg,
            fitness_goal=user.fitness_goal,
            activity_level=user.activity_level,
            dietary_preference=user.dietary_preference,
            experience_level=user.experience_level,
            workout_location=user.workout_location,
            workout_days_per_week=user.workout_days_per_week,
            medical_conditions=user.medical_conditions,
            allergies=user.allergies,
            created_at=user.created_at,
            updated_at=user.updated_at,
            bmi=stats["bmi"],
            bmr=stats["bmr"],
            tdee=stats["tdee"]
        )
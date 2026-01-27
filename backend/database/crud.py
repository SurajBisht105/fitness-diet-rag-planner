# backend/database/crud.py
"""CRUD operations for database models."""

from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import date, datetime, timedelta

from backend.database.models import (
    User, WeightLog, MeasurementLog, 
    WorkoutLog, CalorieLog, WorkoutPlanDB, DietPlanDB
)
from backend.models.user import UserProfileCreate, UserProfileUpdate


class UserCRUD:
    """CRUD operations for User model."""
    
    @staticmethod
    def create(db: Session, user: UserProfileCreate) -> User:
        """Create a new user."""
        db_user = User(**user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def get_by_id(db: Session, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email."""
        return db.query(User).filter(User.email == email.lower()).first()
    
    @staticmethod
    def update(db: Session, user_id: str, user_update: UserProfileUpdate) -> Optional[User]:
        """Update user profile."""
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            update_data = user_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_user, field, value)
            db.commit()
            db.refresh(db_user)
        return db_user
    
    @staticmethod
    def delete(db: Session, user_id: str) -> bool:
        """Delete user."""
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            db.delete(db_user)
            db.commit()
            return True
        return False


class ProgressCRUD:
    """CRUD operations for progress tracking."""
    
    @staticmethod
    def log_weight(db: Session, user_id: str, weight_kg: float, 
                   log_date: date, notes: Optional[str] = None) -> WeightLog:
        """Log weight entry."""
        log = WeightLog(
            user_id=user_id,
            weight_kg=weight_kg,
            date=datetime.combine(log_date, datetime.min.time()),
            notes=notes
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
    
    @staticmethod
    def get_weight_history(db: Session, user_id: str, 
                          days: int = 30) -> List[WeightLog]:
        """Get weight history for user."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        return db.query(WeightLog).filter(
            WeightLog.user_id == user_id,
            WeightLog.date >= cutoff_date
        ).order_by(desc(WeightLog.date)).all()
    
    @staticmethod
    def log_measurements(db: Session, user_id: str, 
                        measurements: dict) -> MeasurementLog:
        """Log body measurements."""
        log = MeasurementLog(user_id=user_id, **measurements)
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
    
    @staticmethod
    def get_measurement_history(db: Session, user_id: str,
                               days: int = 90) -> List[MeasurementLog]:
        """Get measurement history."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        return db.query(MeasurementLog).filter(
            MeasurementLog.user_id == user_id,
            MeasurementLog.date >= cutoff_date
        ).order_by(desc(MeasurementLog.date)).all()
    
    @staticmethod
    def log_workout(db: Session, user_id: str, workout_data: dict) -> WorkoutLog:
        """Log workout completion."""
        log = WorkoutLog(user_id=user_id, **workout_data)
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
    
    @staticmethod
    def get_workout_history(db: Session, user_id: str,
                           days: int = 30) -> List[WorkoutLog]:
        """Get workout history."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        return db.query(WorkoutLog).filter(
            WorkoutLog.user_id == user_id,
            WorkoutLog.date >= cutoff_date
        ).order_by(desc(WorkoutLog.date)).all()
    
    @staticmethod
    def log_calories(db: Session, user_id: str, calorie_data: dict) -> CalorieLog:
        """Log daily calorie intake."""
        log = CalorieLog(user_id=user_id, **calorie_data)
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
    
    @staticmethod
    def get_calorie_history(db: Session, user_id: str,
                           days: int = 30) -> List[CalorieLog]:
        """Get calorie history."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        return db.query(CalorieLog).filter(
            CalorieLog.user_id == user_id,
            CalorieLog.date >= cutoff_date
        ).order_by(desc(CalorieLog.date)).all()


class PlanCRUD:
    """CRUD operations for workout and diet plans."""
    
    @staticmethod
    def save_workout_plan(db: Session, user_id: str, plan_data: dict) -> WorkoutPlanDB:
        """Save workout plan."""
        # Deactivate previous plans
        db.query(WorkoutPlanDB).filter(
            WorkoutPlanDB.user_id == user_id,
            WorkoutPlanDB.is_active == True
        ).update({"is_active": False})
        
        plan = WorkoutPlanDB(
            user_id=user_id,
            plan_name=plan_data.get("plan_name", "Custom Workout Plan"),
            description=plan_data.get("description", ""),
            plan_data=plan_data,
            sources=plan_data.get("sources", [])
        )
        db.add(plan)
        db.commit()
        db.refresh(plan)
        return plan
    
    @staticmethod
    def get_active_workout_plan(db: Session, user_id: str) -> Optional[WorkoutPlanDB]:
        """Get active workout plan for user."""
        return db.query(WorkoutPlanDB).filter(
            WorkoutPlanDB.user_id == user_id,
            WorkoutPlanDB.is_active == True
        ).first()
    
    @staticmethod
    def save_diet_plan(db: Session, user_id: str, plan_data: dict) -> DietPlanDB:
        """Save diet plan."""
        # Deactivate previous plans
        db.query(DietPlanDB).filter(
            DietPlanDB.user_id == user_id,
            DietPlanDB.is_active == True
        ).update({"is_active": False})
        
        plan = DietPlanDB(
            user_id=user_id,
            plan_name=plan_data.get("plan_name", "Custom Diet Plan"),
            description=plan_data.get("description", ""),
            plan_data=plan_data,
            sources=plan_data.get("sources", [])
        )
        db.add(plan)
        db.commit()
        db.refresh(plan)
        return plan
    
    @staticmethod
    def get_active_diet_plan(db: Session, user_id: str) -> Optional[DietPlanDB]:
        """Get active diet plan for user."""
        return db.query(DietPlanDB).filter(
            DietPlanDB.user_id == user_id,
            DietPlanDB.is_active == True
        ).first()
    
    @staticmethod
    def get_plan_history(db: Session, user_id: str, 
                        plan_type: str = "workout") -> List:
        """Get plan history."""
        model = WorkoutPlanDB if plan_type == "workout" else DietPlanDB
        return db.query(model).filter(
            model.user_id == user_id
        ).order_by(desc(model.created_at)).limit(10).all()
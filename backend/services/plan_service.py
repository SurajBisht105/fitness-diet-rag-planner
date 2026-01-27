# backend/services/plan_service.py
"""Plan generation service."""

from typing import Dict, Optional
from sqlalchemy.orm import Session

from backend.database.crud import PlanCRUD, UserCRUD
from backend.database.models import User
from backend.rag.chain import get_rag_chain
from backend.services.progress_service import ProgressService
from backend.services.calorie_service import CalorieCalculator


class PlanService:
    """Service for generating and managing fitness/diet plans."""
    
    def __init__(self):
        self.rag_chain = get_rag_chain()
        self.progress_service = ProgressService()
        self.calorie_calculator = CalorieCalculator()
    
    def generate_plan(
        self,
        db: Session,
        user_id: str,
        plan_type: str = "both",
        custom_query: Optional[str] = None
    ) -> Dict:
        """
        Generate a personalized fitness/diet plan using RAG.
        
        Args:
            db: Database session
            user_id: User ID
            plan_type: "workout", "diet", or "both"
            custom_query: Optional custom user request
            
        Returns:
            Generated plan with sources
        """
        # Get user profile
        user = UserCRUD.get_by_id(db, user_id)
        if not user:
            raise ValueError("User not found")
        
        # Convert to profile dict
        user_profile = self._user_to_profile_dict(user)
        
        # Get progress context
        progress_data = self.progress_service.get_progress_context_for_rag(db, user_id)
        
        # Generate default query if not provided
        if not custom_query:
            custom_query = self._generate_default_query(user_profile, plan_type)
        
        # Generate plan using RAG
        result = self.rag_chain.generate_plan(
            user_profile=user_profile,
            user_query=custom_query,
            plan_type=plan_type,
            progress_data=progress_data
        )
        
        # Save plans to database
        if plan_type in ["workout", "both"]:
            workout_plan_data = {
                "plan_name": f"{user_profile['fitness_goal'].title()} Workout Plan",
                "description": "AI-generated personalized workout plan",
                "plan_content": result["response"],
                "sources": result["sources"]
            }
            PlanCRUD.save_workout_plan(db, user_id, workout_plan_data)
        
        if plan_type in ["diet", "both"]:
            diet_plan_data = {
                "plan_name": f"{user_profile['dietary_preference'].title()} Diet Plan",
                "description": "AI-generated personalized diet plan",
                "plan_content": result["response"],
                "sources": result["sources"]
            }
            PlanCRUD.save_diet_plan(db, user_id, diet_plan_data)
        
        return result
    
    def generate_workout_plan(self, db: Session, user_id: str) -> Dict:
        """Generate only a workout plan."""
        user = UserCRUD.get_by_id(db, user_id)
        if not user:
            raise ValueError("User not found")
        
        user_profile = self._user_to_profile_dict(user)
        progress_data = self.progress_service.get_progress_context_for_rag(db, user_id)
        
        result = self.rag_chain.generate_workout_plan(user_profile, progress_data)
        
        # Save plan
        plan_data = {
            "plan_name": f"{user_profile['fitness_goal'].title()} Workout Plan",
            "description": "AI-generated workout plan",
            "plan_content": result["plan"],
            "sources": result["sources"]
        }
        saved_plan = PlanCRUD.save_workout_plan(db, user_id, plan_data)
        
        return {
            "plan_id": saved_plan.id,
            "plan": result["plan"],
            "sources": result["sources"]
        }
    
    def generate_diet_plan(self, db: Session, user_id: str) -> Dict:
        """Generate only a diet plan."""
        user = UserCRUD.get_by_id(db, user_id)
        if not user:
            raise ValueError("User not found")
        
        user_profile = self._user_to_profile_dict(user)
        progress_data = self.progress_service.get_progress_context_for_rag(db, user_id)
        
        result = self.rag_chain.generate_diet_plan(user_profile, progress_data)
        
        # Save plan
        plan_data = {
            "plan_name": f"{user_profile['dietary_preference'].title()} Diet Plan",
            "description": "AI-generated diet plan",
            "plan_content": result["plan"],
            "stats": result["stats"],
            "sources": result["sources"]
        }
        saved_plan = PlanCRUD.save_diet_plan(db, user_id, plan_data)
        
        return {
            "plan_id": saved_plan.id,
            "plan": result["plan"],
            "stats": result["stats"],
            "sources": result["sources"]
        }
    
    def get_active_plans(self, db: Session, user_id: str) -> Dict:
        """Get user's active workout and diet plans."""
        workout_plan = PlanCRUD.get_active_workout_plan(db, user_id)
        diet_plan = PlanCRUD.get_active_diet_plan(db, user_id)
        
        return {
            "workout_plan": workout_plan.plan_data if workout_plan else None,
            "diet_plan": diet_plan.plan_data if diet_plan else None
        }
    
    def regenerate_plan_with_progress(
        self,
        db: Session,
        user_id: str,
        plan_type: str
    ) -> Dict:
        """Regenerate plan considering progress data."""
        user = UserCRUD.get_by_id(db, user_id)
        if not user:
            raise ValueError("User not found")
        
        user_profile = self._user_to_profile_dict(user)
        progress_data = self.progress_service.get_progress_context_for_rag(db, user_id)
        
        # Build progress-aware query
        query = self._build_progress_aware_query(progress_data, plan_type)
        
        return self.generate_plan(db, user_id, plan_type, query)
    
    def _user_to_profile_dict(self, user: User) -> Dict:
        """Convert User model to profile dictionary."""
        return {
            "name": user.name,
            "age": user.age,
            "gender": user.gender,
            "height_cm": user.height_cm,
            "weight_kg": user.weight_kg,
            "fitness_goal": user.fitness_goal,
            "activity_level": user.activity_level,
            "dietary_preference": user.dietary_preference,
            "experience_level": user.experience_level,
            "workout_location": user.workout_location,
            "workout_days_per_week": user.workout_days_per_week,
            "medical_conditions": user.medical_conditions,
            "allergies": user.allergies
        }
    
    def _generate_default_query(self, user_profile: Dict, plan_type: str) -> str:
        """Generate a default query based on user profile and plan type."""
        goal = user_profile.get("fitness_goal", "general fitness")
        days = user_profile.get("workout_days_per_week", 4)
        diet_pref = user_profile.get("dietary_preference", "balanced")
        
        if plan_type == "workout":
            return f"Create a complete {days}-day workout plan for {goal} at {user_profile.get('experience_level')} level"
        elif plan_type == "diet":
            return f"Create a {diet_pref} diet plan optimized for {goal}"
        else:
            return f"Create a complete {days}-day workout and {diet_pref} diet plan for {goal}"
    
    def _build_progress_aware_query(self, progress_data: Dict, plan_type: str) -> str:
        """Build a query that incorporates progress insights."""
        base_query = []
        
        if progress_data.get("weight_trend"):
            trend = progress_data["weight_trend"]
            if trend == "maintaining":
                base_query.append("I've plateaued and need adjustments to continue progress")
            elif trend == "losing" and progress_data.get("weight_change", 0) < -3:
                base_query.append("I'm losing weight faster than expected, may need to adjust")
        
        if progress_data.get("workout_completion", 0) < 60:
            base_query.append("I'm struggling with workout consistency, need a more manageable plan")
        
        if progress_data.get("calorie_adherence", 0) < 70:
            base_query.append("I'm having trouble following my diet, need simpler meal options")
        
        if base_query:
            return f"Based on my progress: {'; '.join(base_query)}. Please generate an updated {plan_type} plan."
        else:
            return f"Generate an updated {plan_type} plan based on my current progress."
        
# backend/services/__init__.py
"""Services package initialization - Lazy imports."""

def get_user_service():
    from backend.services.user_service import UserService
    return UserService()

def get_plan_service():
    from backend.services.plan_service import PlanService
    return PlanService()

def get_progress_service():
    from backend.services.progress_service import ProgressService
    return ProgressService()

def get_calorie_calculator():
    from backend.services.calorie_service import CalorieCalculator
    return CalorieCalculator()

# For backward compatibility
from backend.services.user_service import UserService
from backend.services.calorie_service import CalorieCalculator
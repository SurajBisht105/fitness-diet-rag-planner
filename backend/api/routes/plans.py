# backend/api/routes/plans.py
"""Plan generation endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from backend.database.connection import get_db
from backend.models.plan import PlanGenerationRequest, PlanGenerationResponse
from backend.services.plan_service import PlanService

router = APIRouter()
plan_service = PlanService()


@router.post("/generate", response_model=dict)
async def generate_plan(
    request: PlanGenerationRequest,
    db: Session = Depends(get_db)
):
    """Generate a personalized fitness/diet plan using RAG."""
    try:
        result = plan_service.generate_plan(
            db=db,
            user_id=request.user_id,
            plan_type=request.plan_type,
            custom_query=request.additional_preferences
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating plan: {str(e)}")


@router.post("/{user_id}/workout")
async def generate_workout_plan(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Generate a workout plan."""
    try:
        return plan_service.generate_workout_plan(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{user_id}/diet")
async def generate_diet_plan(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Generate a diet plan."""
    try:
        return plan_service.generate_diet_plan(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{user_id}/active")
async def get_active_plans(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get user's active plans."""
    return plan_service.get_active_plans(db, user_id)


@router.post("/{user_id}/regenerate/{plan_type}")
async def regenerate_plan(
    user_id: str,
    plan_type: str,
    db: Session = Depends(get_db)
):
    """Regenerate plan based on progress."""
    if plan_type not in ["workout", "diet", "both"]:
        raise HTTPException(status_code=400, detail="Invalid plan type")
    
    try:
        return plan_service.regenerate_plan_with_progress(db, user_id, plan_type)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
# backend/services/progress_service.py
"""Progress tracking service."""

from typing import List, Dict, Optional
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session

from backend.database.crud import ProgressCRUD
from backend.database.models import User
from backend.models.progress import ProgressSummary, ProgressChartData


class ProgressService:
    """Service for progress tracking operations."""
    
    def log_weight(self, db: Session, user_id: str, weight_kg: float,
                   log_date: date, notes: Optional[str] = None) -> Dict:
        """Log a weight entry."""
        log = ProgressCRUD.log_weight(db, user_id, weight_kg, log_date, notes)
        return {
            "id": log.id,
            "weight_kg": log.weight_kg,
            "date": log.date.isoformat(),
            "notes": log.notes
        }
    
    def log_measurements(self, db: Session, user_id: str, 
                        measurements: Dict) -> Dict:
        """Log body measurements."""
        log = ProgressCRUD.log_measurements(db, user_id, measurements)
        return {
            "id": log.id,
            "date": log.date.isoformat(),
            "measurements": {
                "chest_cm": log.chest_cm,
                "waist_cm": log.waist_cm,
                "hips_cm": log.hips_cm,
                "biceps_cm": log.biceps_cm,
                "thighs_cm": log.thighs_cm,
                "body_fat_percentage": log.body_fat_percentage
            }
        }
    
    def log_workout(self, db: Session, user_id: str, 
                   workout_data: Dict) -> Dict:
        """Log workout completion."""
        log = ProgressCRUD.log_workout(db, user_id, workout_data)
        return {
            "id": log.id,
            "date": log.date.isoformat(),
            "completed": log.completed,
            "duration_mins": log.duration_mins
        }
    
    def log_calories(self, db: Session, user_id: str,
                    calorie_data: Dict) -> Dict:
        """Log daily calorie intake."""
        log = ProgressCRUD.log_calories(db, user_id, calorie_data)
        return {
            "id": log.id,
            "date": log.date.isoformat(),
            "total_calories": log.total_calories,
            "macros": {
                "protein": log.total_protein,
                "carbs": log.total_carbs,
                "fats": log.total_fats
            }
        }
    
    def get_progress_summary(self, db: Session, user_id: str, 
                            days: int = 30) -> ProgressSummary:
        """Get a summary of user's progress."""
        # Get weight history
        weight_logs = ProgressCRUD.get_weight_history(db, user_id, days)
        
        # Get workout history
        workout_logs = ProgressCRUD.get_workout_history(db, user_id, days)
        
        # Get calorie history
        calorie_logs = ProgressCRUD.get_calorie_history(db, user_id, days)
        
        # Calculate weight metrics
        if weight_logs and len(weight_logs) >= 2:
            starting_weight = weight_logs[-1].weight_kg
            current_weight = weight_logs[0].weight_kg
            weight_change = current_weight - starting_weight
            
            if weight_change < -0.5:
                weight_trend = "losing"
            elif weight_change > 0.5:
                weight_trend = "gaining"
            else:
                weight_trend = "maintaining"
        else:
            starting_weight = current_weight = weight_logs[0].weight_kg if weight_logs else 0
            weight_change = 0
            weight_trend = "insufficient_data"
        
        # Calculate workout completion
        total_planned = len(workout_logs) if workout_logs else 0
        total_completed = sum(1 for log in workout_logs if log.completed) if workout_logs else 0
        completion_rate = (total_completed / total_planned * 100) if total_planned > 0 else 0
        
        # Calculate calorie adherence
        if calorie_logs:
            # This would need user's target calories to calculate properly
            avg_calories = sum(log.total_calories for log in calorie_logs) / len(calorie_logs)
            adherence_rate = 85.0  # Placeholder - would calculate based on target
        else:
            avg_calories = 0
            adherence_rate = 0
        
        # Generate insights
        insights = self._generate_insights(
            weight_trend, completion_rate, adherence_rate, weight_change
        )
        
        # Generate adjustment recommendations
        adjustments = self._generate_adjustments(
            weight_trend, completion_rate, adherence_rate
        )
        
        return ProgressSummary(
            user_id=user_id,
            period_start=date.today() - timedelta(days=days),
            period_end=date.today(),
            starting_weight=starting_weight,
            current_weight=current_weight,
            weight_change=round(weight_change, 1),
            weight_trend=weight_trend,
            total_workouts_planned=total_planned,
            total_workouts_completed=total_completed,
            completion_rate=round(completion_rate, 1),
            avg_daily_calories=round(avg_calories, 0),
            calorie_target=2000,  # Would come from user profile
            adherence_rate=round(adherence_rate, 1),
            insights=insights,
            adjustments_needed=adjustments
        )
    
    def get_chart_data(self, db: Session, user_id: str, 
                       days: int = 30) -> ProgressChartData:
        """Get data formatted for charts."""
        # Weight data
        weight_logs = ProgressCRUD.get_weight_history(db, user_id, days)
        weight_data = [
            {"date": log.date.strftime("%Y-%m-%d"), "weight": log.weight_kg}
            for log in reversed(weight_logs)
        ]
        
        # Calorie data
        calorie_logs = ProgressCRUD.get_calorie_history(db, user_id, days)
        calorie_data = [
            {
                "date": log.date.strftime("%Y-%m-%d"),
                "intake": log.total_calories,
                "target": 2000  # Would come from user profile
            }
            for log in reversed(calorie_logs)
        ]
        
        # Workout data by week
        workout_logs = ProgressCRUD.get_workout_history(db, user_id, days)
        workout_data = self._aggregate_workouts_by_week(workout_logs)
        
        # Measurement data
        measurement_logs = ProgressCRUD.get_measurement_history(db, user_id, days)
        measurement_data = [
            {
                "date": log.date.strftime("%Y-%m-%d"),
                "waist": log.waist_cm,
                "chest": log.chest_cm,
                "biceps": log.biceps_cm
            }
            for log in reversed(measurement_logs)
        ]
        
        return ProgressChartData(
            weight_data=weight_data,
            calorie_data=calorie_data,
            workout_data=workout_data,
            measurement_data=measurement_data
        )
    
    def get_progress_context_for_rag(self, db: Session, user_id: str) -> Dict:
        """Get progress data formatted for RAG context."""
        summary = self.get_progress_summary(db, user_id, days=30)
        
        weight_logs = ProgressCRUD.get_weight_history(db, user_id, 30)
        weight_history = [log.weight_kg for log in weight_logs]
        
        calorie_logs = ProgressCRUD.get_calorie_history(db, user_id, 14)
        avg_adherence = sum(log.total_calories for log in calorie_logs) / len(calorie_logs) if calorie_logs else 0
        
        return {
            "weight_history": weight_history,
            "weight_trend": summary.weight_trend,
            "weight_change": summary.weight_change,
            "workout_completion": summary.completion_rate,
            "calorie_adherence": summary.adherence_rate,
            "insights": summary.insights
        }
    
    def _generate_insights(self, weight_trend: str, completion_rate: float,
                          adherence_rate: float, weight_change: float) -> List[str]:
        """Generate insights based on progress data."""
        insights = []
        
        if weight_trend == "losing" and weight_change < -2:
            insights.append("Great progress! You're consistently losing weight.")
        elif weight_trend == "gaining" and weight_change > 2:
            insights.append("You're gaining weight as planned for muscle building.")
        elif weight_trend == "maintaining":
            insights.append("Your weight is stable. Adjust calories if you want to change.")
        
        if completion_rate >= 80:
            insights.append("Excellent workout consistency! Keep it up!")
        elif completion_rate >= 50:
            insights.append("Good effort! Try to improve workout consistency.")
        elif completion_rate > 0:
            insights.append("Workout consistency needs improvement. Start with smaller goals.")
        
        if adherence_rate >= 80:
            insights.append("You're following your nutrition plan well.")
        elif adherence_rate >= 50:
            insights.append("Nutrition adherence is moderate. Focus on meal prep.")
        
        return insights if insights else ["Start logging your progress to get personalized insights."]
    
    def _generate_adjustments(self, weight_trend: str, completion_rate: float,
                             adherence_rate: float) -> List[str]:
        """Generate adjustment recommendations."""
        adjustments = []
        
        if weight_trend == "maintaining" and completion_rate < 50:
            adjustments.append("Increase workout frequency to break the plateau.")
        
        if adherence_rate < 70:
            adjustments.append("Consider meal prepping to improve nutrition adherence.")
        
        if completion_rate < 60:
            adjustments.append("Try scheduling workouts at a consistent time each day.")
        
        return adjustments if adjustments else ["Keep following your current plan!"]
    
    def _aggregate_workouts_by_week(self, workout_logs: List) -> List[Dict]:
        """Aggregate workout logs by week."""
        if not workout_logs:
            return []
        
        weeks = {}
        for log in workout_logs:
            week_num = log.date.isocalendar()[1]
            week_key = f"Week {week_num}"
            
            if week_key not in weeks:
                weeks[week_key] = {"completed": 0, "planned": 0}
            
            weeks[week_key]["planned"] += 1
            if log.completed:
                weeks[week_key]["completed"] += 1
        
        return [
            {"week": week, "completed": data["completed"], "planned": data["planned"]}
            for week, data in weeks.items()
        ]
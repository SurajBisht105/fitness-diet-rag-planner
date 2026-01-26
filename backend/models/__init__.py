# backend/models/__init__.py
"""Models package initialization."""

from backend.models.user import (
    UserProfileCreate,
    UserProfileUpdate,
    UserProfileResponse,
    UserStats,
    FitnessGoal,
    ActivityLevel,
    DietaryPreference,
    ExperienceLevel,
    Gender,
    WorkoutLocation
)

from backend.models.plan import (
    Exercise,
    WorkoutDay,
    WorkoutPlan,
    Meal,
    DailyDiet,
    DietPlan,
    PlanGenerationRequest,
    PlanGenerationResponse
)

from backend.models.progress import (
    WeightLog,
    MeasurementLog,
    WorkoutLog,
    CalorieLog,
    ProgressSummary,
    ProgressChartData
)

from backend.models.rag import (
    DocumentChunk,
    RetrievalQuery,
    RetrievedDocument,
    RAGQuery,
    RAGResponse,
    IngestionRequest,
    IngestionResponse
)

__all__ = [
    # User models
    "UserProfileCreate",
    "UserProfileUpdate", 
    "UserProfileResponse",
    "UserStats",
    "FitnessGoal",
    "ActivityLevel",
    "DietaryPreference",
    "ExperienceLevel",
    "Gender",
    "WorkoutLocation",
    # Plan models
    "Exercise",
    "WorkoutDay",
    "WorkoutPlan",
    "Meal",
    "DailyDiet",
    "DietPlan",
    "PlanGenerationRequest",
    "PlanGenerationResponse",
    # Progress models
    "WeightLog",
    "MeasurementLog",
    "WorkoutLog",
    "CalorieLog",
    "ProgressSummary",
    "ProgressChartData",
    # RAG models
    "DocumentChunk",
    "RetrievalQuery",
    "RetrievedDocument",
    "RAGQuery",
    "RAGResponse",
    "IngestionRequest",
    "IngestionResponse"
]
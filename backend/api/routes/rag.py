# backend/api/routes/rag.py
"""RAG-specific endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.models.rag import (
    RAGQuery, RAGResponse, RetrievalQuery,
    IngestionRequest, IngestionResponse
)
from backend.rag.chain import get_rag_chain
from backend.rag.retriever import get_fitness_retriever
from backend.rag.ingestion import get_ingester
from backend.services.progress_service import ProgressService
from backend.database.crud import UserCRUD
from datetime import datetime

router = APIRouter()


@router.post("/query", response_model=RAGResponse)
async def query_rag(
    query: RAGQuery,
    db: Session = Depends(get_db)
):
    """Query the RAG system."""
    # Get user profile
    user = UserCRUD.get_by_id(db, query.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get progress context if requested
    progress_data = None
    if query.include_progress_context:
        progress_service = ProgressService()
        progress_data = progress_service.get_progress_context_for_rag(db, query.user_id)
    
    # Build user profile dict
    user_profile = {
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
    
    # Query RAG chain
    rag_chain = get_rag_chain()
    result = rag_chain.generate_plan(
        user_profile=user_profile,
        user_query=query.query,
        plan_type=query.plan_type,
        progress_data=progress_data
    )
    
    return RAGResponse(
        response=result["response"],
        sources=[
            {
                "id": s.get("id", ""),
                "content": "",  # Don't return full content
                "metadata": s,
                "score": s.get("score", 0)
            }
            for s in result.get("sources", [])
        ],
        confidence_score=0.85,  # Would calculate based on retrieval scores
        follow_up_questions=result.get("follow_up_questions", []),
        generated_at=datetime.utcnow()
    )


@router.post("/retrieve")
async def retrieve_documents(
    query: RetrievalQuery
):
    """Retrieve relevant documents without generation."""
    retriever = get_fitness_retriever()
    
    # Build minimal user profile for retrieval
    user_profile = {
        "experience_level": query.filter_level or "all",
        "workout_location": "both"
    }
    
    if query.filter_type == "workout":
        docs = retriever.retrieve_workout_context(
            query.query, user_profile, query.top_k
        )
    elif query.filter_type == "diet":
        docs = retriever.retrieve_diet_context(
            query.query, user_profile, query.top_k
        )
    else:
        result = retriever.retrieve_combined_context(
            query.query, user_profile, query.top_k // 2
        )
        docs = result["workouts"] + result["diets"]
    
    return {
        "documents": [
            {
                "id": doc.metadata.get("id"),
                "content": doc.page_content[:500],
                "metadata": doc.metadata,
                "score": doc.metadata.get("score")
            }
            for doc in docs
        ]
    }


@router.post("/ingest", response_model=IngestionResponse)
async def ingest_documents(
    request: IngestionRequest
):
    """Ingest documents into the vector store."""
    try:
        ingester = get_ingester()
        
        if request.overwrite:
            namespace = f"{request.document_type}s"
            ingester.clear_namespace(namespace)
        
        total_chunks = 0
        for doc in request.documents:
            chunks = ingester.ingest_single_document(doc, request.document_type)
            total_chunks += chunks
        
        return IngestionResponse(
            success=True,
            documents_processed=len(request.documents),
            chunks_created=total_chunks,
            message="Documents ingested successfully"
        )
    except Exception as e:
        return IngestionResponse(
            success=False,
            documents_processed=0,
            chunks_created=0,
            message=f"Error during ingestion: {str(e)}"
        )


@router.post("/ingest/bulk")
async def bulk_ingest(
    data_dir: str = "data/raw"
):
    """Bulk ingest all data from directory."""
    try:
        ingester = get_ingester()
        stats = ingester.ingest_all(data_dir)
        
        return {
            "success": True,
            "stats": stats,
            "message": "Bulk ingestion completed"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Bulk ingestion failed: {str(e)}"
        )


@router.get("/stats")
async def get_rag_stats():
    """Get RAG system statistics."""
    from backend.rag.vectorstore import get_pinecone_manager
    
    pm = get_pinecone_manager()
    stats = pm.get_stats()
    
    return {
        "vectorstore": "pinecone",
        "index_stats": stats
    }
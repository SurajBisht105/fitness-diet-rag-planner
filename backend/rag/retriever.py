# backend/rag/retriever.py
"""Document retrieval with context awareness."""

from typing import List, Dict, Optional
from langchain_core.documents import Document


class FitnessRetriever:
    """Custom retriever for fitness and diet documents."""
    
    def __init__(self):
        """Initialize the retriever."""
        self._pinecone_manager = None
        self._embedding_manager = None
    
    @property
    def pinecone_manager(self):
        if self._pinecone_manager is None:
            from backend.rag.vectorstore import get_pinecone_manager
            self._pinecone_manager = get_pinecone_manager()
        return self._pinecone_manager
    
    @property
    def embedding_manager(self):
        if self._embedding_manager is None:
            from backend.rag.embeddings import get_embedding_manager
            self._embedding_manager = get_embedding_manager()
        return self._embedding_manager
    
    @property
    def is_available(self) -> bool:
        """Check if retriever is available."""
        return (self.pinecone_manager.is_available and 
                self.embedding_manager.is_available)
    
    def retrieve_workout_context(self, query: str, user_profile: Dict,
                                  top_k: int = 5) -> List[Document]:
        """Retrieve relevant workout documents based on user profile."""
        if not self.is_available:
            return self._get_fallback_workout_docs()
        
        filter_dict = self._build_workout_filter(user_profile)
        enhanced_query = self._enhance_query(query, user_profile, "workout")
        
        results = self.pinecone_manager.query(
            query=enhanced_query,
            top_k=top_k,
            namespace="workouts",
            filter_dict=filter_dict
        )
        
        docs = self._results_to_documents(results)
        return docs if docs else self._get_fallback_workout_docs()
    
    def retrieve_diet_context(self, query: str, user_profile: Dict,
                               top_k: int = 5) -> List[Document]:
        """Retrieve relevant diet documents based on user profile."""
        if not self.is_available:
            return self._get_fallback_diet_docs()
        
        filter_dict = self._build_diet_filter(user_profile)
        enhanced_query = self._enhance_query(query, user_profile, "diet")
        
        results = self.pinecone_manager.query(
            query=enhanced_query,
            top_k=top_k,
            namespace="diets",
            filter_dict=filter_dict
        )
        
        docs = self._results_to_documents(results)
        return docs if docs else self._get_fallback_diet_docs()
    
    def retrieve_combined_context(self, query: str, user_profile: Dict,
                                   top_k_each: int = 3) -> Dict[str, List[Document]]:
        """Retrieve both workout and diet context."""
        workout_docs = self.retrieve_workout_context(query, user_profile, top_k_each)
        diet_docs = self.retrieve_diet_context(query, user_profile, top_k_each)
        
        return {
            'workouts': workout_docs,
            'diets': diet_docs
        }
    
    def _build_workout_filter(self, user_profile: Dict) -> Optional[Dict]:
        """Build Pinecone filter for workouts."""
        filters = {}
        
        if user_profile.get('experience_level'):
            filters['experience_level'] = {"$eq": user_profile['experience_level']}
        
        if user_profile.get('workout_location'):
            location = user_profile['workout_location']
            if location != 'both':
                filters['location'] = {"$eq": location}
        
        return filters if filters else None
    
    def _build_diet_filter(self, user_profile: Dict) -> Optional[Dict]:
        """Build Pinecone filter for diets."""
        filters = {}
        
        if user_profile.get('dietary_preference'):
            filters['dietary_type'] = {"$eq": user_profile['dietary_preference']}
        
        return filters if filters else None
    
    def _enhance_query(self, query: str, user_profile: Dict, context_type: str) -> str:
        """Enhance query with user profile context."""
        enhancements = []
        
        if context_type == "workout":
            if user_profile.get('fitness_goal'):
                enhancements.append(f"Goal: {user_profile['fitness_goal']}")
            if user_profile.get('experience_level'):
                enhancements.append(f"Level: {user_profile['experience_level']}")
            if user_profile.get('workout_location'):
                enhancements.append(f"Location: {user_profile['workout_location']}")
        
        elif context_type == "diet":
            if user_profile.get('dietary_preference'):
                enhancements.append(f"Preference: {user_profile['dietary_preference']}")
            if user_profile.get('fitness_goal'):
                enhancements.append(f"Goal: {user_profile['fitness_goal']}")
        
        if enhancements:
            return f"{query} [{' | '.join(enhancements)}]"
        return query
    
    def _results_to_documents(self, results: List[Dict]) -> List[Document]:
        """Convert query results to LangChain documents."""
        documents = []
        for result in results:
            doc = Document(
                page_content=result.get('text', ''),
                metadata={
                    'id': result.get('id'),
                    'score': result.get('score'),
                    **result.get('metadata', {})
                }
            )
            documents.append(doc)
        return documents
    
    def _get_fallback_workout_docs(self) -> List[Document]:
        """Get fallback workout documents when RAG is unavailable."""
        return [
            Document(
                page_content="""
                # General Workout Guidelines
                
                ## Beginner Full Body Workout (3 days/week)
                - Squats: 3 sets x 10-12 reps
                - Push-ups: 3 sets x 8-12 reps
                - Dumbbell Rows: 3 sets x 10 reps each arm
                - Lunges: 3 sets x 10 reps each leg
                - Plank: 3 sets x 30 seconds
                
                ## Intermediate Split (4 days/week)
                Day 1: Chest & Triceps
                Day 2: Back & Biceps
                Day 3: Rest
                Day 4: Legs
                Day 5: Shoulders & Core
                
                ## Important Notes
                - Always warm up for 5-10 minutes
                - Rest 60-90 seconds between sets
                - Stay hydrated
                - Progressive overload is key
                """,
                metadata={'type': 'workout', 'source': 'fallback', 'score': 0.5}
            )
        ]
    
    def _get_fallback_diet_docs(self) -> List[Document]:
        """Get fallback diet documents when RAG is unavailable."""
        return [
            Document(
                page_content="""
                # General Diet Guidelines
                
                ## Indian Vegetarian High Protein Foods
                - Paneer: 18g protein per 100g
                - Dal (Lentils): 9g protein per 100g
                - Chickpeas: 19g protein per 100g
                - Greek Yogurt: 10g protein per 100g
                - Soy chunks: 52g protein per 100g
                
                ## Sample Meal Plan (2000 kcal)
                Breakfast: Paneer bhurji with 2 rotis (500 kcal)
                Snack: Sprouts chaat (200 kcal)
                Lunch: Rajma chawal with salad (600 kcal)
                Snack: Protein shake with banana (250 kcal)
                Dinner: Dal with roti and vegetables (450 kcal)
                
                ## Macro Split for Muscle Gain
                - Protein: 30% (150g)
                - Carbs: 45% (225g)
                - Fats: 25% (55g)
                """,
                metadata={'type': 'diet', 'source': 'fallback', 'score': 0.5}
            )
        ]


# Singleton instance
_fitness_retriever: Optional[FitnessRetriever] = None


def get_fitness_retriever() -> FitnessRetriever:
    """Get or create singleton fitness retriever."""
    global _fitness_retriever
    if _fitness_retriever is None:
        _fitness_retriever = FitnessRetriever()
    return _fitness_retriever
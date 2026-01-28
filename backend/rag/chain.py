# backend/rag/chain.py
"""LangChain RAG chain implementation."""

from typing import Dict, List, Optional, Any
from backend.config import settings
from backend.rag.prompts import get_rag_prompt, get_workout_prompt, get_diet_prompt


class FitnessRAGChain:
    """RAG chain for fitness and diet plan generation."""
    
    def __init__(self):
        """Initialize the RAG chain."""
        self._retriever = None
        self._llm = None
        self._calorie_calculator = None
    
    @property
    def retriever(self):
        if self._retriever is None:
            from backend.rag.retriever import get_fitness_retriever
            self._retriever = get_fitness_retriever()
        return self._retriever
    
    @property
    def llm(self):
        if self._llm is None:
            self._llm = self._initialize_llm()
        return self._llm
    
    @property
    def calorie_calculator(self):
        if self._calorie_calculator is None:
            from backend.services.calorie_service import CalorieCalculator
            self._calorie_calculator = CalorieCalculator()
        return self._calorie_calculator
    
    def _initialize_llm(self):
        """Initialize the LLM."""
        if settings.GOOGLE_API_KEY:
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
                return ChatGoogleGenerativeAI(
                    model=settings.GEMINI_MODEL,
                    google_api_key=settings.GOOGLE_API_KEY,
                    temperature=0.3,
                    max_output_tokens=4096,
                )
            except Exception as e:
                print(f"Warning: Could not initialize Gemini LLM: {e}")
        
        # Return None if no LLM available
        return None
    
    @property
    def is_available(self) -> bool:
        """Check if RAG chain is available."""
        return self.llm is not None
    
    def generate_plan(self, user_profile: Dict, user_query: str,
                      plan_type: str = "both",
                      progress_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate a personalized fitness/diet plan using RAG."""
        
        # Calculate calorie and macro targets
        stats = self.calorie_calculator.calculate_all(user_profile)
        
        # Retrieve relevant context
        context = self.retriever.retrieve_combined_context(
            query=user_query,
            user_profile=user_profile
        )
        
        # Format context for prompt
        workout_context = self._format_documents(context['workouts'])
        diet_context = self._format_documents(context['diets'])
        
        # Format progress context
        progress_context = self._format_progress(progress_data) if progress_data else "No previous progress data available."
        
        # If LLM is not available, return context-based response
        if not self.is_available:
            return self._generate_fallback_response(
                user_profile, stats, workout_context, diet_context, context
            )
        
        # Build prompt inputs
        prompt_inputs = {
            "user_name": user_profile.get("name", "User"),
            "age": user_profile.get("age"),
            "gender": user_profile.get("gender"),
            "height_cm": user_profile.get("height_cm"),
            "weight_kg": user_profile.get("weight_kg"),
            "bmi": round(stats["bmi"], 1),
            "fitness_goal": user_profile.get("fitness_goal"),
            "activity_level": user_profile.get("activity_level"),
            "experience_level": user_profile.get("experience_level"),
            "workout_location": user_profile.get("workout_location"),
            "workout_days": user_profile.get("workout_days_per_week"),
            "dietary_preference": user_profile.get("dietary_preference"),
            "medical_conditions": user_profile.get("medical_conditions", "None reported"),
            "allergies": user_profile.get("allergies", "None reported"),
            "daily_calories": stats["daily_calories"],
            "protein_g": stats["protein_g"],
            "carbs_g": stats["carbs_g"],
            "fats_g": stats["fats_g"],
            "progress_context": progress_context,
            "workout_context": workout_context,
            "diet_context": diet_context,
            "user_query": user_query
        }
        
        try:
            # Generate response using RAG prompt
            from langchain_core.output_parsers import StrOutputParser
            prompt = get_rag_prompt()
            chain = prompt | self.llm | StrOutputParser()
            response = chain.invoke(prompt_inputs)
        except Exception as e:
            print(f"Error generating with LLM: {e}")
            return self._generate_fallback_response(
                user_profile, stats, workout_context, diet_context, context
            )
        
        # Extract sources
        sources = self._extract_sources(context)
        
        # Generate follow-up questions
        follow_ups = self._generate_follow_ups(user_profile, plan_type)
        
        return {
            "response": response,
            "sources": sources,
            "stats": stats,
            "follow_up_questions": follow_ups
        }
    
    def generate_workout_plan(self, user_profile: Dict,
                               progress_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate a detailed workout plan."""
        query = f"Complete {user_profile.get('workout_days_per_week')}-day workout plan for {user_profile.get('fitness_goal')} goal"
        
        context = self.retriever.retrieve_workout_context(
            query=query,
            user_profile=user_profile,
            top_k=7
        )
        
        workout_context = self._format_documents(context)
        
        if not self.is_available:
            return {
                "plan": workout_context,
                "sources": [{"id": doc.metadata.get("id"), "score": doc.metadata.get("score")} for doc in context]
            }
        
        try:
            from langchain_core.output_parsers import StrOutputParser
            prompt = get_workout_prompt()
            prompt_inputs = {
                "user_profile": self._format_user_profile(user_profile),
                "workout_context": workout_context,
                "workout_days": user_profile.get("workout_days_per_week"),
                "fitness_goal": user_profile.get("fitness_goal"),
                "experience_level": user_profile.get("experience_level"),
                "workout_location": user_profile.get("workout_location")
            }
            
            chain = prompt | self.llm | StrOutputParser()
            response = chain.invoke(prompt_inputs)
        except Exception as e:
            print(f"Error generating workout plan: {e}")
            response = workout_context
        
        return {
            "plan": response,
            "sources": [{"id": doc.metadata.get("id"), "score": doc.metadata.get("score")} for doc in context]
        }
    
    def generate_diet_plan(self, user_profile: Dict,
                            progress_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate a detailed diet plan."""
        stats = self.calorie_calculator.calculate_all(user_profile)
        
        query = f"Diet plan for {user_profile.get('dietary_preference')} with {stats['daily_calories']} calories"
        
        context = self.retriever.retrieve_diet_context(
            query=query,
            user_profile=user_profile,
            top_k=7
        )
        
        diet_context = self._format_documents(context)
        
        if not self.is_available:
            return {
                "plan": diet_context,
                "stats": stats,
                "sources": [{"id": doc.metadata.get("id"), "score": doc.metadata.get("score")} for doc in context]
            }
        
        try:
            from langchain_core.output_parsers import StrOutputParser
            prompt = get_diet_prompt()
            prompt_inputs = {
                "user_profile": self._format_user_profile(user_profile),
                "diet_context": diet_context,
                "daily_calories": stats["daily_calories"],
                "protein_g": stats["protein_g"],
                "carbs_g": stats["carbs_g"],
                "fats_g": stats["fats_g"],
                "dietary_preference": user_profile.get("dietary_preference"),
                "allergies": user_profile.get("allergies", "None")
            }
            
            chain = prompt | self.llm | StrOutputParser()
            response = chain.invoke(prompt_inputs)
        except Exception as e:
            print(f"Error generating diet plan: {e}")
            response = diet_context
        
        return {
            "plan": response,
            "stats": stats,
            "sources": [{"id": doc.metadata.get("id"), "score": doc.metadata.get("score")} for doc in context]
        }
    
    def _generate_fallback_response(self, user_profile: Dict, stats: Dict,
                                     workout_context: str, diet_context: str,
                                     context: Dict) -> Dict[str, Any]:
        """Generate a fallback response when LLM is unavailable."""
        response = f"""
# Personalized Fitness & Diet Plan for {user_profile.get('name', 'User')}

## Your Stats
- **BMI:** {stats['bmi']:.1f} ({stats['bmi_category']})
- **Daily Calories:** {stats['daily_calories']} kcal
- **Protein:** {stats['protein_g']}g | **Carbs:** {stats['carbs_g']}g | **Fats:** {stats['fats_g']}g

## Workout Plan
{workout_context}

## Diet Plan
{diet_context}

---
*Note: This is a basic plan generated from our knowledge base. For more personalized AI-generated plans, please configure the Google API key.*
"""
        
        return {
            "response": response,
            "sources": self._extract_sources(context),
            "stats": stats,
            "follow_up_questions": [
                "Do you have any specific exercises you'd like to include?",
                "Are there any foods you particularly enjoy?",
                "What time do you prefer to workout?"
            ]
        }
    
    def _format_documents(self, documents: List) -> str:
        """Format retrieved documents for prompt context."""
        if not documents:
            return "No relevant documents found."
        
        formatted = []
        for i, doc in enumerate(documents, 1):
            content = doc.page_content if hasattr(doc, 'page_content') else str(doc)
            metadata = doc.metadata if hasattr(doc, 'metadata') else {}
            score = metadata.get('score', 'N/A')
            score_str = f"{score:.2f}" if isinstance(score, float) else str(score)
            source_info = f"[Source {i}, Relevance: {score_str}]"
            formatted.append(f"{source_info}\n{content}")
        
        return "\n\n---\n\n".join(formatted)
    
    def _format_progress(self, progress_data: Dict) -> str:
        """Format progress data for context."""
        if not progress_data:
            return "No progress data available."
        
        parts = []
        
        if progress_data.get("weight_history"):
            weights = progress_data["weight_history"][-5:]
            parts.append(f"Recent weights: {', '.join([f'{w:.1f}kg' for w in weights])}")
        
        if progress_data.get("workout_completion"):
            rate = progress_data["workout_completion"]
            parts.append(f"Workout completion rate: {rate:.1f}%")
        
        if progress_data.get("calorie_adherence"):
            adherence = progress_data["calorie_adherence"]
            parts.append(f"Calorie adherence: {adherence:.1f}%")
        
        return "\n".join(parts) if parts else "No progress data available."
    
    def _format_user_profile(self, profile: Dict) -> str:
        """Format user profile as readable string."""
        return f"""
- Name: {profile.get('name', 'User')}
- Age: {profile.get('age')} years
- Gender: {profile.get('gender')}
- Height: {profile.get('height_cm')} cm
- Weight: {profile.get('weight_kg')} kg
- Goal: {profile.get('fitness_goal')}
- Activity Level: {profile.get('activity_level')}
- Experience: {profile.get('experience_level')}
- Workout Location: {profile.get('workout_location')}
- Days/Week: {profile.get('workout_days_per_week')}
- Diet Preference: {profile.get('dietary_preference')}
"""
    
    def _extract_sources(self, context: Dict) -> List[Dict]:
        """Extract source information from retrieved documents."""
        sources = []
        
        for doc in context.get('workouts', []):
            sources.append({
                "id": doc.metadata.get("id"),
                "type": "workout",
                "score": doc.metadata.get("score"),
                "title": doc.metadata.get("title", "Workout Routine")
            })
        
        for doc in context.get('diets', []):
            sources.append({
                "id": doc.metadata.get("id"),
                "type": "diet",
                "score": doc.metadata.get("score"),
                "title": doc.metadata.get("title", "Diet Plan")
            })
        
        return sources
    
    def _generate_follow_ups(self, user_profile: Dict, plan_type: str) -> List[str]:
        """Generate relevant follow-up questions."""
        questions = []
        
        if not user_profile.get("medical_conditions"):
            questions.append("Do you have any medical conditions or injuries I should consider?")
        
        if not user_profile.get("allergies"):
            questions.append("Do you have any food allergies or intolerances?")
        
        if plan_type in ["workout", "both"]:
            questions.append("Do you have access to specific gym equipment?")
            questions.append("How much time can you dedicate to each workout session?")
        
        if plan_type in ["diet", "both"]:
            questions.append("Do you prefer meal prepping or cooking fresh daily?")
            questions.append("Are there any specific foods you dislike?")
        
        return questions[:3]


# Singleton instance
_rag_chain: Optional[FitnessRAGChain] = None


def get_rag_chain() -> FitnessRAGChain:
    """Get or create singleton RAG chain."""
    global _rag_chain
    if _rag_chain is None:
        _rag_chain = FitnessRAGChain()
    return _rag_chain
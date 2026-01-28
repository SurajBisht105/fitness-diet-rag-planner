# backend/rag/prompts.py
"""Prompt templates for RAG-based generation."""

from langchain_core.prompts import PromptTemplate


# Main RAG prompt template
RAG_PROMPT_TEMPLATE = """You are an expert AI Fitness and Diet Planner. Using ONLY the retrieved workout routines, diet charts, and user progress data below, generate a safe, personalized fitness and diet plan.

CRITICAL RULES:
1. ONLY use information from the provided context documents
2. NEVER make up exercises, diets, or nutritional information
3. If information is missing, explicitly ask follow-up questions
4. NEVER provide medical advice
5. Always prioritize safety

=== USER PROFILE ===
Name: {user_name}
Age: {age} years | Gender: {gender}
Height: {height_cm} cm | Weight: {weight_kg} kg | BMI: {bmi}
Fitness Goal: {fitness_goal}
Activity Level: {activity_level}
Experience Level: {experience_level}
Workout Location: {workout_location}
Workout Days per Week: {workout_days}
Dietary Preference: {dietary_preference}
Medical Conditions: {medical_conditions}
Allergies: {allergies}

=== CALORIE & MACRO TARGETS ===
Daily Calories: {daily_calories} kcal
Protein: {protein_g}g | Carbohydrates: {carbs_g}g | Fats: {fats_g}g

=== USER PROGRESS ===
{progress_context}

=== RETRIEVED WORKOUT CONTEXT ===
{workout_context}

=== RETRIEVED DIET CONTEXT ===
{diet_context}

=== USER REQUEST ===
{user_query}

Generate a comprehensive, personalized response addressing the user's request. Include specific exercises with sets/reps and meals with portions. Cite your sources.

Response:"""


WORKOUT_PLAN_PROMPT = """Based on the retrieved workout context and user profile, create a detailed weekly workout plan.

=== USER PROFILE ===
{user_profile}

=== RETRIEVED WORKOUT ROUTINES ===
{workout_context}

=== REQUIREMENTS ===
Generate a {workout_days}-day workout plan that:
1. Aligns with the user's {fitness_goal} goal
2. Is appropriate for {experience_level} level
3. Can be performed at {workout_location}
4. Includes proper warm-up and cool-down
5. Has progressive overload suggestions

Format the plan with:
- Day and focus area
- Exercises with sets, reps, and rest periods
- Notes on form and progression
- Estimated duration

Weekly Workout Plan:"""


DIET_PLAN_PROMPT = """Based on the retrieved diet context and user profile, create a detailed daily meal plan.

=== USER PROFILE ===
{user_profile}

=== CALORIE TARGETS ===
Daily Calories: {daily_calories} kcal
Protein: {protein_g}g | Carbs: {carbs_g}g | Fats: {fats_g}g

=== DIETARY REQUIREMENTS ===
Preference: {dietary_preference}
Allergies: {allergies}

=== RETRIEVED DIET CONTEXT ===
{diet_context}

=== REQUIREMENTS ===
Generate a daily meal plan that:
1. Meets the calorie and macro targets
2. Follows {dietary_preference} guidelines
3. Avoids any allergens mentioned
4. Includes 5-6 meals with portions and macros
5. Uses easily available ingredients

Daily Meal Plan:"""


def get_rag_prompt() -> PromptTemplate:
    """Get the main RAG prompt template."""
    return PromptTemplate(
        template=RAG_PROMPT_TEMPLATE,
        input_variables=[
            "user_name", "age", "gender", "height_cm", "weight_kg", "bmi",
            "fitness_goal", "activity_level", "experience_level",
            "workout_location", "workout_days", "dietary_preference",
            "medical_conditions", "allergies", "daily_calories",
            "protein_g", "carbs_g", "fats_g", "progress_context",
            "workout_context", "diet_context", "user_query"
        ]
    )


def get_workout_prompt() -> PromptTemplate:
    """Get workout plan generation prompt."""
    return PromptTemplate(
        template=WORKOUT_PLAN_PROMPT,
        input_variables=[
            "user_profile", "workout_context", "workout_days",
            "fitness_goal", "experience_level", "workout_location"
        ]
    )


def get_diet_prompt() -> PromptTemplate:
    """Get diet plan generation prompt."""
    return PromptTemplate(
        template=DIET_PLAN_PROMPT,
        input_variables=[
            "user_profile", "diet_context", "daily_calories",
            "protein_g", "carbs_g", "fats_g", "dietary_preference", "allergies"
        ]
    )
# backend/services/calorie_service.py
"""Calorie and macro calculation service."""

from typing import Dict
from backend.models.user import ActivityLevel, FitnessGoal


class CalorieCalculator:
    """Calculates BMR, TDEE, and macros based on user profile."""
    
    # Activity level multipliers
    ACTIVITY_MULTIPLIERS = {
        ActivityLevel.SEDENTARY: 1.2,
        ActivityLevel.LIGHTLY_ACTIVE: 1.375,
        ActivityLevel.MODERATELY_ACTIVE: 1.55,
        ActivityLevel.VERY_ACTIVE: 1.725,
        ActivityLevel.EXTREMELY_ACTIVE: 1.9
    }
    
    # Goal-based calorie adjustments
    GOAL_ADJUSTMENTS = {
        FitnessGoal.LEAN: -300,  # Slight deficit for lean/toned look
        FitnessGoal.MUSCLE_GAIN: 300,  # Surplus for muscle building
        FitnessGoal.FAT_LOSS: -500  # Moderate deficit for fat loss
    }
    
    # Macro ratios by goal (protein%, carbs%, fats%)
    MACRO_RATIOS = {
        FitnessGoal.LEAN: {"protein": 0.30, "carbs": 0.40, "fats": 0.30},
        FitnessGoal.MUSCLE_GAIN: {"protein": 0.30, "carbs": 0.45, "fats": 0.25},
        FitnessGoal.FAT_LOSS: {"protein": 0.35, "carbs": 0.30, "fats": 0.35}
    }
    
    def calculate_bmi(self, weight_kg: float, height_cm: float) -> float:
        """Calculate Body Mass Index."""
        height_m = height_cm / 100
        return weight_kg / (height_m ** 2)
    
    def get_bmi_category(self, bmi: float) -> str:
        """Get BMI category."""
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"
    
    def calculate_bmr(self, weight_kg: float, height_cm: float, 
                      age: int, gender: str) -> float:
        """
        Calculate Basal Metabolic Rate using Mifflin-St Jeor equation.
        
        This is more accurate than Harris-Benedict for modern populations.
        """
        if gender.lower() == "male":
            bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
        else:
            bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
        
        return round(bmr, 0)
    
    def calculate_tdee(self, bmr: float, activity_level: str) -> float:
        """Calculate Total Daily Energy Expenditure."""
        try:
            activity = ActivityLevel(activity_level)
            multiplier = self.ACTIVITY_MULTIPLIERS.get(activity, 1.55)
        except ValueError:
            multiplier = 1.55  # Default to moderately active
        
        return round(bmr * multiplier, 0)
    
    def calculate_daily_calories(self, tdee: float, fitness_goal: str) -> int:
        """Calculate daily calorie target based on goal."""
        try:
            goal = FitnessGoal(fitness_goal)
            adjustment = self.GOAL_ADJUSTMENTS.get(goal, 0)
        except ValueError:
            adjustment = 0
        
        calories = tdee + adjustment
        
        # Ensure minimum safe calories
        min_calories = 1200  # General minimum
        return max(int(calories), min_calories)
    
    def calculate_macros(self, daily_calories: int, fitness_goal: str) -> Dict[str, int]:
        """Calculate macro nutrient targets in grams."""
        try:
            goal = FitnessGoal(fitness_goal)
            ratios = self.MACRO_RATIOS.get(goal, self.MACRO_RATIOS[FitnessGoal.LEAN])
        except ValueError:
            ratios = self.MACRO_RATIOS[FitnessGoal.LEAN]
        
        # Calculate grams (protein & carbs = 4 cal/g, fats = 9 cal/g)
        protein_cals = daily_calories * ratios["protein"]
        carbs_cals = daily_calories * ratios["carbs"]
        fats_cals = daily_calories * ratios["fats"]
        
        return {
            "protein_g": int(protein_cals / 4),
            "carbs_g": int(carbs_cals / 4),
            "fats_g": int(fats_cals / 9)
        }
    
    def calculate_all(self, user_profile: Dict) -> Dict:
        """
        Calculate all fitness metrics for a user.
        
        Args:
            user_profile: Dictionary with user profile data
            
        Returns:
            Dictionary with all calculated metrics
        """
        weight = user_profile.get("weight_kg")
        height = user_profile.get("height_cm")
        age = user_profile.get("age")
        gender = user_profile.get("gender")
        activity = user_profile.get("activity_level")
        goal = user_profile.get("fitness_goal")
        
        # Calculate metrics
        bmi = self.calculate_bmi(weight, height)
        bmi_category = self.get_bmi_category(bmi)
        bmr = self.calculate_bmr(weight, height, age, gender)
        tdee = self.calculate_tdee(bmr, activity)
        daily_calories = self.calculate_daily_calories(tdee, goal)
        macros = self.calculate_macros(daily_calories, goal)
        
        # Calculate ideal weight range (BMI 18.5-24.9)
        height_m = height / 100
        ideal_weight_min = round(18.5 * (height_m ** 2), 1)
        ideal_weight_max = round(24.9 * (height_m ** 2), 1)
        
        # Water intake recommendation (ml)
        water_ml = int(weight * 35)  # 35ml per kg body weight
        
        return {
            "bmi": round(bmi, 1),
            "bmi_category": bmi_category,
            "bmr": int(bmr),
            "tdee": int(tdee),
            "daily_calories": daily_calories,
            "protein_g": macros["protein_g"],
            "carbs_g": macros["carbs_g"],
            "fats_g": macros["fats_g"],
            "ideal_weight_min": ideal_weight_min,
            "ideal_weight_max": ideal_weight_max,
            "water_ml": water_ml,
            "macro_percentages": {
                "protein": int(self.MACRO_RATIOS.get(FitnessGoal(goal), {}).get("protein", 0.3) * 100),
                "carbs": int(self.MACRO_RATIOS.get(FitnessGoal(goal), {}).get("carbs", 0.4) * 100),
                "fats": int(self.MACRO_RATIOS.get(FitnessGoal(goal), {}).get("fats", 0.3) * 100)
            }
        }
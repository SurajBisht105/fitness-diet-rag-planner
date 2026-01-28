# scripts/generate_sample_data.py
"""Script to generate sample data for testing."""

import sys
import os
import json
from pathlib import Path
from datetime import date, timedelta
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def generate_sample_workouts():
    """Generate sample workout data."""
    workouts = {
        "items": [
            {
                "name": "Beginner Full Body Workout",
                "type": "strength",
                "level": "beginner",
                "goal": "lean",
                "location": "gym",
                "duration": "45 minutes",
                "description": "Perfect starter workout for gym beginners",
                "warm_up": ["5 min treadmill walk", "Arm circles", "Leg swings"],
                "exercises": [
                    {"name": "Goblet Squat", "sets": 3, "reps": "12", "rest": "60s", "muscle_group": "legs"},
                    {"name": "Dumbbell Bench Press", "sets": 3, "reps": "10", "rest": "60s", "muscle_group": "chest"},
                    {"name": "Lat Pulldown", "sets": 3, "reps": "10", "rest": "60s", "muscle_group": "back"},
                    {"name": "Dumbbell Shoulder Press", "sets": 3, "reps": "10", "rest": "60s", "muscle_group": "shoulders"},
                    {"name": "Plank", "sets": 3, "reps": "30 seconds", "rest": "45s", "muscle_group": "core"}
                ],
                "cool_down": ["5 min stretching", "Deep breathing"],
                "progression": "Add weight when you can complete all reps with good form"
            },
            {
                "name": "Fat Burning HIIT",
                "type": "cardio",
                "level": "intermediate",
                "goal": "fat_loss",
                "location": "home",
                "duration": "25 minutes",
                "description": "High intensity interval training for maximum fat burn",
                "warm_up": ["Jumping jacks - 1 min", "High knees - 1 min"],
                "exercises": [
                    {"name": "Burpees", "sets": 4, "reps": "30 seconds", "rest": "15s", "muscle_group": "full_body"},
                    {"name": "Mountain Climbers", "sets": 4, "reps": "30 seconds", "rest": "15s", "muscle_group": "core"},
                    {"name": "Jump Squats", "sets": 4, "reps": "30 seconds", "rest": "15s", "muscle_group": "legs"},
                    {"name": "Push-ups", "sets": 4, "reps": "30 seconds", "rest": "15s", "muscle_group": "chest"},
                    {"name": "Bicycle Crunches", "sets": 4, "reps": "30 seconds", "rest": "15s", "muscle_group": "core"}
                ],
                "cool_down": ["Walking - 2 min", "Stretching - 3 min"],
                "progression": "Increase work intervals or decrease rest"
            },
            {
                "name": "Advanced Push Day",
                "type": "strength",
                "level": "advanced",
                "goal": "muscle_gain",
                "location": "gym",
                "duration": "75 minutes",
                "description": "Intense push workout for experienced lifters",
                "warm_up": ["5 min cardio", "Rotator cuff warmup", "Light push-ups"],
                "exercises": [
                    {"name": "Barbell Bench Press", "sets": 5, "reps": "5", "rest": "180s", "muscle_group": "chest"},
                    {"name": "Incline Dumbbell Press", "sets": 4, "reps": "8", "rest": "90s", "muscle_group": "chest"},
                    {"name": "Standing Overhead Press", "sets": 4, "reps": "6", "rest": "120s", "muscle_group": "shoulders"},
                    {"name": "Dips", "sets": 4, "reps": "10", "rest": "90s", "muscle_group": "triceps"},
                    {"name": "Cable Flyes", "sets": 3, "reps": "12", "rest": "60s", "muscle_group": "chest"},
                    {"name": "Lateral Raises", "sets": 4, "reps": "15", "rest": "45s", "muscle_group": "shoulders"},
                    {"name": "Tricep Pushdowns", "sets": 3, "reps": "12", "rest": "45s", "muscle_group": "triceps"}
                ],
                "cool_down": ["Chest stretches", "Shoulder stretches", "Tricep stretches"],
                "progression": "Follow 5/3/1 or linear progression for main lifts"
            }
        ]
    }
    return workouts


def generate_sample_diets():
    """Generate sample diet data."""
    diets = {
        "items": [
            {
                "name": "Balanced Indian Diet - 2000 calories",
                "dietary_type": "indian_veg",
                "goal": "lean",
                "calories": 2000,
                "description": "Balanced vegetarian Indian diet for maintaining fitness",
                "macros": {"protein": 100, "carbs": 250, "fats": 65},
                "meals": [
                    {
                        "name": "Breakfast",
                        "time": "8:00 AM",
                        "items": [
                            {"name": "Oats Upma", "portion": "1 bowl"},
                            {"name": "Boiled Eggs", "portion": "2"},
                            {"name": "Green Tea", "portion": "1 cup"}
                        ],
                        "calories": 400,
                        "protein": 20,
                        "carbs": 50,
                        "fats": 12
                    },
                    {
                        "name": "Lunch",
                        "time": "1:00 PM",
                        "items": [
                            {"name": "Dal", "portion": "1 cup"},
                            {"name": "Roti", "portion": "2"},
                            {"name": "Sabzi", "portion": "1 cup"},
                            {"name": "Salad", "portion": "1 bowl"},
                            {"name": "Curd", "portion": "1/2 cup"}
                        ],
                        "calories": 550,
                        "protein": 25,
                        "carbs": 70,
                        "fats": 18
                    },
                    {
                        "name": "Evening Snack",
                        "time": "5:00 PM",
                        "items": [
                            {"name": "Sprouts Chaat", "portion": "1 cup"},
                            {"name": "Buttermilk", "portion": "1 glass"}
                        ],
                        "calories": 200,
                        "protein": 12,
                        "carbs": 25,
                        "fats": 5
                    },
                    {
                        "name": "Dinner",
                        "time": "8:00 PM",
                        "items": [
                            {"name": "Grilled Paneer", "portion": "100g"},
                            {"name": "Roti", "portion": "2"},
                            {"name": "Mixed Veg", "portion": "1 cup"}
                        ],
                        "calories": 450,
                        "protein": 28,
                        "carbs": 45,
                        "fats": 18
                    }
                ],
                "tips": [
                    "Drink 8-10 glasses of water daily",
                    "Avoid processed foods",
                    "Eat dinner at least 2 hours before bed"
                ],
                "grocery_list": ["Paneer", "Lentils", "Whole wheat flour", "Fresh vegetables", "Curd", "Eggs"]
            }
        ]
    }
    return diets


def main():
    """Generate sample data files."""
    print("🚀 Generating sample data...")
    
    # Create directories
    data_dir = Path("data/raw")
    (data_dir / "workouts").mkdir(parents=True, exist_ok=True)
    (data_dir / "diets").mkdir(parents=True, exist_ok=True)
    
    # Generate workouts
    workouts = generate_sample_workouts()
    workout_file = data_dir / "workouts" / "sample_workouts.json"
    with open(workout_file, 'w') as f:
        json.dump(workouts, f, indent=2)
    print(f"✅ Created {workout_file}")
    
    # Generate diets
    diets = generate_sample_diets()
    diet_file = data_dir / "diets" / "sample_diets.json"
    with open(diet_file, 'w') as f:
        json.dump(diets, f, indent=2)
    print(f"✅ Created {diet_file}")
    
    print("\n✅ Sample data generation complete!")


if __name__ == "__main__":
    main()
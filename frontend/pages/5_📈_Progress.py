# frontend/pages/5_📈_Progress.py
"""Progress Tracking Page."""

import streamlit as st
import sys
from pathlib import Path
from datetime import date

current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

from api_client import api_client
from components import (
    render_weight_chart, render_calorie_chart,
    render_workout_completion_chart, render_progress_summary_cards,
    render_insight_cards
)

st.set_page_config(page_title="Progress", page_icon="📈", layout="wide")

st.title("📈 Progress Tracking")

# Check login
if not st.session_state.get("user_id"):
    st.warning("⚠️ Please login first")
    if st.button("👤 Go to Profile"):
        st.switch_page("pages/2_👤_Profile.py")
    st.stop()

user_id = st.session_state["user_id"]

# Tabs
tab1, tab2, tab3 = st.tabs(["📝 Log", "📊 Charts", "💡 Insights"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⚖️ Log Weight")
        with st.form("weight_form"):
            weight = st.number_input("Weight (kg)", 30.0, 300.0, 70.0, 0.1)
            w_date = st.date_input("Date", date.today())
            w_notes = st.text_input("Notes (optional)")
            if st.form_submit_button("Log Weight", use_container_width=True):
                result = api_client.log_weight(user_id, weight, w_date.isoformat(), w_notes)
                if "error" not in result:
                    st.success("✅ Weight logged!")
                else:
                    st.error(result["error"])
    
    with col2:
        st.markdown("### 🏋️ Log Workout")
        with st.form("workout_form"):
            wo_date = st.date_input("Date", date.today(), key="wo_date")
            completed = st.checkbox("Completed", True)
            duration = st.number_input("Duration (min)", 0, 180, 45)
            energy = st.slider("Energy (1-10)", 1, 10, 7)
            if st.form_submit_button("Log Workout", use_container_width=True):
                result = api_client.log_workout(user_id, {
                    "date": wo_date.isoformat(),
                    "workout_day_id": "general",
                    "completed": completed,
                    "duration_mins": duration,
                    "energy_level": energy,
                    "exercises_completed": []
                })
                if "error" not in result:
                    st.success("✅ Workout logged!")
                else:
                    st.error(result["error"])
    
    st.markdown("---")
    st.markdown("### 🍽️ Log Calories")
    with st.form("cal_form"):
        c_date = st.date_input("Date", date.today(), key="c_date")
        col1, col2, col3, col4 = st.columns(4)
        cals = col1.number_input("Calories", 0, 10000, 2000)
        prot = col2.number_input("Protein (g)", 0, 500, 100)
        carbs = col3.number_input("Carbs (g)", 0, 1000, 200)
        fats = col4.number_input("Fats (g)", 0, 500, 70)
        water = st.slider("Water (L)", 0.0, 5.0, 2.0, 0.25)
        
        if st.form_submit_button("Log Calories", use_container_width=True):
            result = api_client.log_calories(user_id, {
                "date": c_date.isoformat(),
                "meals": [],
                "total_calories": cals,
                "total_protein": prot,
                "total_carbs": carbs,
                "total_fats": fats,
                "water_liters": water
            })
            if "error" not in result:
                st.success("✅ Calories logged!")
            else:
                st.error(result["error"])

with tab2:
    days = st.selectbox("Time Range", [7, 14, 30, 60, 90], 2, format_func=lambda x: f"Last {x} days")
    
    with st.spinner("Loading..."):
        data = api_client.get_chart_data(user_id, days)
    
    if "error" not in data:
        st.markdown("### ⚖️ Weight")
        render_weight_chart(data.get("weight_data", []))
        st.markdown("### 🍽️ Calories")
        render_calorie_chart(data.get("calorie_data", []))
        st.markdown("### 🏋️ Workouts")
        render_workout_completion_chart(data.get("workout_data", []))
    else:
        st.warning("No data yet. Start logging!")

with tab3:
    with st.spinner("Analyzing..."):
        summary = api_client.get_progress_summary(user_id, 30)
    
    if "error" not in summary:
        render_progress_summary_cards(summary)
        st.markdown("---")
        render_insight_cards(
            summary.get("insights", []),
            summary.get("adjustments_needed", [])
        )
    else:
        st.info("Log progress to see insights!")
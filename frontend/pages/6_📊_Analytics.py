# frontend/pages/6_📊_Analytics.py
"""Analytics Page."""

import streamlit as st
import sys
from pathlib import Path

current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

from api_client import api_client
from components import render_weight_chart, render_calorie_chart, render_workout_completion_chart

st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")

st.title("📊 Analytics Dashboard")

if not st.session_state.get("user_id"):
    st.warning("⚠️ Please login first")
    if st.button("👤 Go to Profile"):
        st.switch_page("pages/2_👤_Profile.py")
    st.stop()

user_id = st.session_state["user_id"]

# Filters
col1, col2 = st.columns([1, 3])
with col1:
    days = st.selectbox("Range", [7, 14, 30, 60, 90], 2, format_func=lambda x: f"{x} days")

# Load data
with st.spinner("Loading..."):
    data = api_client.get_chart_data(user_id, days)
    summary = api_client.get_progress_summary(user_id, days)
    stats = api_client.get_user_stats(user_id)

if "error" not in data:
    # KPIs
    st.markdown("### 📈 Key Metrics")
    k1, k2, k3, k4 = st.columns(4)
    
    k1.metric("Weight Change", f"{summary.get('weight_change', 0):+.1f} kg")
    k2.metric("Workout Rate", f"{summary.get('completion_rate', 0):.0f}%")
    k3.metric("Avg Calories", f"{summary.get('avg_daily_calories', 0):.0f}")
    k4.metric("BMI", f"{stats.get('bmi', 0):.1f}" if "error" not in stats else "N/A")
    
    st.markdown("---")
    
    # Charts
    st.markdown("### ⚖️ Weight Trend")
    render_weight_chart(data.get("weight_data", []))
    
    st.markdown("### 🍽️ Calorie Tracking")
    render_calorie_chart(data.get("calorie_data", []))
    
    st.markdown("### 🏋️ Workout Completion")
    render_workout_completion_chart(data.get("workout_data", []))
else:
    st.warning("No data available. Start logging your progress!")
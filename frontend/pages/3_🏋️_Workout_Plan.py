# frontend/pages/3_🏋️_Workout_Plan.py
"""Workout Plan Page."""

import streamlit as st
import sys
from pathlib import Path

current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

from api_client import api_client

st.set_page_config(page_title="Workout Plan", page_icon="🏋️", layout="wide")

st.title("🏋️ Your Workout Plan")

# Check if logged in
if not st.session_state.get("user_id"):
    st.warning("⚠️ Please create or login to your profile first")
    if st.button("👤 Go to Profile", use_container_width=True):
        st.switch_page("pages/2_👤_Profile.py")
    st.stop()

user_id = st.session_state["user_id"]
user_data = st.session_state.get("user_data", {})

# Sidebar
with st.sidebar:
    st.markdown(f"### 👤 {user_data.get('name', 'User')}")
    st.markdown(f"**Goal:** {user_data.get('fitness_goal', 'N/A').replace('_', ' ').title()}")
    st.markdown(f"**Level:** {user_data.get('experience_level', 'N/A').title()}")
    st.markdown(f"**Location:** {user_data.get('workout_location', 'N/A').title()}")
    st.markdown(f"**Days/Week:** {user_data.get('workout_days_per_week', 0)}")
    
    st.markdown("---")
    
    regenerate = st.button("🔄 Generate New Plan", use_container_width=True)
    
    st.markdown("---")
    
    custom_request = st.text_area(
        "Custom Preferences",
        placeholder="E.g., Focus on upper body, include more cardio, avoid jumping...",
        height=100
    )
    
    if st.button("🎯 Generate Custom Plan", use_container_width=True):
        regenerate = True
        st.session_state["custom_workout_request"] = custom_request

# Main content
if regenerate or "workout_plan" not in st.session_state:
    custom = st.session_state.get("custom_workout_request", custom_request if custom_request else None)
    
    with st.spinner("🤖 AI is generating your personalized workout plan..."):
        try:
            if custom:
                result = api_client.generate_plan(user_id, "workout", custom)
            else:
                result = api_client.generate_workout_plan(user_id)
            
            if "error" not in result:
                st.session_state["workout_plan"] = result
                st.session_state.pop("custom_workout_request", None)
                st.success("✅ Workout plan generated!")
            else:
                st.error(f"❌ Error: {result['error']}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Display plan
if "workout_plan" in st.session_state:
    plan = st.session_state["workout_plan"]
    
    st.markdown("### 📋 Your Weekly Workout Schedule")
    st.markdown("---")
    
    # Show plan content
    if "plan" in plan:
        st.markdown(plan["plan"])
    elif "response" in plan:
        st.markdown(plan["response"])
    else:
        st.info("No plan content. Try generating again.")
    
    # Show sources
    if plan.get("sources"):
        with st.expander("📚 Sources (RAG Context)"):
            for i, source in enumerate(plan["sources"], 1):
                st.caption(f"{i}. {source.get('title', source.get('id', 'Unknown'))}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Log Workout", use_container_width=True):
            st.switch_page("pages/5_📈_Progress.py")
    with col2:
        if st.button("🥗 View Diet Plan", use_container_width=True):
            st.switch_page("pages/4_🥗_Diet_Plan.py")
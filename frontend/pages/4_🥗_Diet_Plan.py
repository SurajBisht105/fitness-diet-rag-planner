# frontend/pages/4_🥗_Diet_Plan.py
"""Diet Plan Page."""

import streamlit as st
import sys
from pathlib import Path

current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

from api_client import api_client
from components import render_macro_cards, render_macro_pie_chart

st.set_page_config(page_title="Diet Plan", page_icon="🥗", layout="wide")

st.title("🥗 Your Diet Plan")

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
    st.markdown(f"**Diet:** {user_data.get('dietary_preference', 'N/A').replace('_', ' ').title()}")
    st.markdown(f"**Goal:** {user_data.get('fitness_goal', 'N/A').replace('_', ' ').title()}")
    
    st.markdown("---")
    
    regenerate = st.button("🔄 Generate New Plan", use_container_width=True)
    
    st.markdown("---")
    
    excluded = st.text_input("🚫 Foods to Avoid", placeholder="E.g., eggs, fish...")
    
    custom_request = st.text_area(
        "Special Requests",
        placeholder="E.g., Simple recipes, more protein, budget-friendly...",
        height=100
    )
    
    if st.button("🎯 Generate Custom Plan", use_container_width=True):
        regenerate = True
        prefs = custom_request or ""
        if excluded:
            prefs = f"{prefs}\nExclude: {excluded}".strip()
        st.session_state["custom_diet_request"] = prefs

# Generate plan
if regenerate or "diet_plan" not in st.session_state:
    custom = st.session_state.get("custom_diet_request")
    
    with st.spinner("🤖 AI is generating your personalized diet plan..."):
        try:
            if custom:
                result = api_client.generate_plan(user_id, "diet", custom)
            else:
                result = api_client.generate_diet_plan(user_id)
            
            if "error" not in result:
                st.session_state["diet_plan"] = result
                st.session_state.pop("custom_diet_request", None)
                st.success("✅ Diet plan generated!")
            else:
                st.error(f"❌ Error: {result['error']}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Display plan
if "diet_plan" in st.session_state:
    plan = st.session_state["diet_plan"]
    
    # Stats
    if plan.get("stats"):
        stats = plan["stats"]
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Calories", f"{stats.get('daily_calories', 0)} kcal")
        col2.metric("Protein", f"{stats.get('protein_g', 0)}g")
        col3.metric("Carbs", f"{stats.get('carbs_g', 0)}g")
        col4.metric("Fats", f"{stats.get('fats_g', 0)}g")
        st.markdown("---")
    
    # Tabs
    tab1, tab2 = st.tabs(["📋 Meal Plan", "📊 Macros"])
    
    with tab1:
        if "plan" in plan:
            st.markdown(plan["plan"])
        elif "response" in plan:
            st.markdown(plan["response"])
        else:
            st.info("No plan content.")
    
    with tab2:
        if plan.get("stats"):
            col1, col2 = st.columns(2)
            with col1:
                render_macro_cards(plan["stats"])
            with col2:
                render_macro_pie_chart({"protein": 30, "carbs": 40, "fats": 30})
    
    # Sources
    if plan.get("sources"):
        with st.expander("📚 Sources"):
            for i, source in enumerate(plan["sources"], 1):
                st.caption(f"{i}. {source.get('title', source.get('id', 'Unknown'))}")
# frontend/pages/2_👤_Profile.py
"""User Profile Page."""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

from api_client import api_client
from components import render_profile_form, render_stats_cards, render_macro_cards

st.set_page_config(page_title="Profile - AI Fitness Planner", page_icon="👤", layout="wide")

st.title("👤 Your Profile")

# Initialize session state
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "user_data" not in st.session_state:
    st.session_state["user_data"] = None

# Tab selection
tab1, tab2 = st.tabs(["📝 Profile", "📊 My Stats"])

with tab1:
    if st.session_state.get("user_data"):
        # Existing user - show update form
        st.success(f"✅ Logged in as **{st.session_state['user_data'].get('name', 'User')}**")
        st.info("Update your profile information below")
        
        profile_data = render_profile_form(existing_data=st.session_state["user_data"])
        
        if profile_data:
            with st.spinner("Updating profile..."):
                result = api_client.update_user(st.session_state["user_id"], profile_data)
                if "error" not in result:
                    st.session_state["user_data"] = result
                    st.success("✅ Profile updated successfully!")
                    st.rerun()
                else:
                    st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
    else:
        # New user or login
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔑 Login")
            login_email = st.text_input("Your Email", placeholder="email@example.com", key="profile_login_email")
            if st.button("Find My Profile", use_container_width=True):
                if login_email:
                    with st.spinner("Looking up..."):
                        result = api_client.get_user_by_email(login_email.strip())
                        if "error" not in result and "id" in result:
                            st.session_state["user_id"] = result["id"]
                            st.session_state["user_data"] = result
                            st.success(f"✅ Welcome back, {result.get('name', 'User')}!")
                            st.rerun()
                        else:
                            st.warning("No profile found. Create one below!")
                else:
                    st.warning("Please enter your email")
        
        with col2:
            st.subheader("✨ New User?")
            st.write("Fill out the form below to create your profile")
        
        st.markdown("---")
        st.subheader("📋 Create New Profile")
        
        profile_data = render_profile_form()
        
        if profile_data:
            with st.spinner("Creating profile..."):
                result = api_client.create_user(profile_data)
                if "error" not in result and "id" in result:
                    st.session_state["user_id"] = result["id"]
                    st.session_state["user_data"] = result
                    st.success("✅ Profile created successfully!")
                    st.balloons()
                    st.rerun()
                else:
                    error = result.get('error', 'Unknown error')
                    if "already exists" in str(error).lower():
                        st.error("❌ An account with this email already exists. Please login instead.")
                    else:
                        st.error(f"❌ Error: {error}")

with tab2:
    if st.session_state.get("user_id"):
        with st.spinner("Loading your stats..."):
            stats = api_client.get_user_stats(st.session_state["user_id"])
        
        if "error" not in stats:
            st.subheader("📈 Your Fitness Statistics")
            render_stats_cards(stats)
            
            st.markdown("---")
            
            st.subheader("🍽️ Daily Macro Targets")
            render_macro_cards(stats)
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 💧 Water Intake")
                water_liters = stats.get('water_ml', 2500) / 1000
                st.markdown(f"**Recommended:** {water_liters:.1f} liters/day")
            
            with col2:
                st.markdown("### ⚖️ Ideal Weight Range")
                st.markdown(f"**Range:** {stats.get('ideal_weight_min', 0):.1f} - {stats.get('ideal_weight_max', 0):.1f} kg")
                current = st.session_state["user_data"].get("weight_kg", 0)
                st.markdown(f"**Current:** {current:.1f} kg")
        else:
            st.error(f"Error loading stats: {stats.get('error')}")
    else:
        st.info("👆 Please create or login to your profile to view your stats")

# Sidebar
with st.sidebar:
    if st.session_state.get("user_data"):
        user = st.session_state["user_data"]
        st.markdown(f"### 👤 {user.get('name', 'User')}")
        st.caption(f"📧 {user.get('email', '')}")
        st.markdown(f"**Goal:** {user.get('fitness_goal', 'N/A').replace('_', ' ').title()}")
        st.markdown(f"**Level:** {user.get('experience_level', 'N/A').title()}")
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state["user_id"] = None
            st.session_state["user_data"] = None
            st.rerun()
    else:
        st.info("Create or login to your profile")
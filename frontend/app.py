# frontend/app.py
"""Main Streamlit application - Home Page."""

import streamlit as st
import sys
from pathlib import Path

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Now import from local files
from api_client import api_client

# Page configuration
st.set_page_config(
    page_title="AI Fitness & Diet Planner",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    .feature-card h3 { margin-top: 0; margin-bottom: 0.5rem; }
    .feature-card p { margin-bottom: 0; opacity: 0.9; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "user_data" not in st.session_state:
    st.session_state["user_data"] = None

# Header
st.markdown('<h1 class="main-header">🏋️ AI Fitness & Diet Planner</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Get personalized workout and diet plans powered by AI and verified fitness data</p>', unsafe_allow_html=True)

# Feature Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>🎯 Goal-Based</h3>
        <p>Lean, muscle gain, or fat loss</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>🤖 AI-Powered</h3>
        <p>RAG technology for accuracy</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>📊 Track Progress</h3>
        <p>Charts & analytics</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <h3>🥗 Indian Diet</h3>
        <p>Veg & non-veg options</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Get Started Section
st.header("🚀 Get Started")

col1, col2 = st.columns(2)

with col1:
    st.subheader("✨ New User?")
    st.write("Create your profile to get personalized workout and diet plans")
    if st.button("📝 Create Profile", key="create_btn", use_container_width=True, type="primary"):
        st.switch_page("pages/2_👤_Profile.py")

with col2:
    st.subheader("🔑 Returning User?")
    email = st.text_input("Enter your email", placeholder="your@email.com", key="login_email")
    if st.button("🔓 Access My Plans", key="login_btn", use_container_width=True):
        if email:
            with st.spinner("Looking up your profile..."):
                result = api_client.get_user_by_email(email.strip())
                if "error" not in result and "id" in result:
                    st.session_state["user_id"] = result["id"]
                    st.session_state["user_data"] = result
                    st.success(f"✅ Welcome back, {result.get('name', 'User')}!")
                    st.switch_page("pages/2_👤_Profile.py")
                else:
                    st.warning("❌ No account found with this email. Please create a profile.")
        else:
            st.warning("Please enter your email address")

st.markdown("---")

# How It Works
st.header("ℹ️ How It Works")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### 1️⃣ Create Profile")
    st.write("Enter your details, goals, and dietary preferences")

with col2:
    st.markdown("### 2️⃣ Get AI Plans")
    st.write("Our RAG system creates personalized workout & diet plans")

with col3:
    st.markdown("### 3️⃣ Track Progress")
    st.write("Log your workouts, weight, and meals")

with col4:
    st.markdown("### 4️⃣ Adapt")
    st.write("Plans evolve based on your progress")

st.markdown("---")

# FAQ
with st.expander("🧠 What is RAG and why does it matter?"):
    st.markdown("""
    **RAG (Retrieval-Augmented Generation)** ensures AI recommendations are grounded in verified data:
    
    - ✅ No made-up exercises or nutrition information
    - ✅ All recommendations come from verified fitness databases
    - ✅ Sources are transparent and traceable
    - ✅ Reduces AI "hallucination" to near zero
    """)

with st.expander("🇮🇳 Do you support Indian diets?"):
    st.markdown("""
    Yes! We have extensive support for Indian dietary preferences:
    
    - 🥬 **Indian Vegetarian**: Paneer, dal, legumes, dairy-based proteins
    - 🍗 **Indian Non-Vegetarian**: Chicken, fish, eggs, mutton
    - 🍲 Traditional recipes adapted for fitness goals
    - 📊 Macro-optimized Indian meal plans
    """)

# Disclaimer
st.markdown("---")
st.caption("""
⚠️ **Disclaimer**: This app provides general fitness and nutrition guidance. 
It is not a substitute for professional medical advice. 
Consult a healthcare provider before starting any new fitness or diet program.
""")

# Sidebar
with st.sidebar:
    st.markdown("## 🏋️ Fitness Planner")
    
    if st.session_state.get("user_id"):
        user = st.session_state.get("user_data", {})
        st.success(f"✅ Logged in as **{user.get('name', 'User')}**")
        st.caption(f"Goal: {user.get('fitness_goal', 'N/A').replace('_', ' ').title()}")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state["user_id"] = None
            st.session_state["user_data"] = None
            st.rerun()
    else:
        st.info("👤 Not logged in")
    
    st.markdown("---")
    
    # Backend status
    st.markdown("### 🔌 Backend Status")
    try:
        health = api_client.health_check()
        if "error" not in health:
            st.success("✅ Online")
        else:
            st.error("❌ Offline")
            st.caption(health.get("error", "Cannot connect"))
    except Exception as e:
        st.error("❌ Offline")
        st.caption("Start backend: `uvicorn backend.main:app --reload`")
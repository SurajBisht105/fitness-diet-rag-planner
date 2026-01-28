# frontend/components.py
"""All UI components for the Streamlit app."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Optional


# ==================== CHART COMPONENTS ====================

def render_weight_chart(weight_data: List[Dict]):
    """Render weight progress chart."""
    if not weight_data:
        st.info("📊 No weight data available yet. Start logging your weight!")
        return
    
    df = pd.DataFrame(weight_data)
    df['date'] = pd.to_datetime(df['date'])
    
    fig = px.line(
        df, x='date', y='weight',
        title='Weight Progress',
        labels={'weight': 'Weight (kg)', 'date': 'Date'},
        markers=True
    )
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Weight (kg)",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_calorie_chart(calorie_data: List[Dict]):
    """Render calorie tracking chart."""
    if not calorie_data:
        st.info("📊 No calorie data available yet. Start logging your meals!")
        return
    
    df = pd.DataFrame(calorie_data)
    df['date'] = pd.to_datetime(df['date'])
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['date'],
        y=df['intake'],
        name='Actual Intake',
        marker_color='#1E88E5'
    ))
    
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['target'],
        name='Target',
        line=dict(color='#FF5722', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title='Daily Calorie Intake vs Target',
        xaxis_title='Date',
        yaxis_title='Calories',
        barmode='group',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_workout_completion_chart(workout_data: List[Dict]):
    """Render workout completion chart."""
    if not workout_data:
        st.info("📊 No workout data available yet. Start logging your workouts!")
        return
    
    df = pd.DataFrame(workout_data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['week'],
        y=df['completed'],
        name='Completed',
        marker_color='#4CAF50'
    ))
    
    fig.add_trace(go.Bar(
        x=df['week'],
        y=df['planned'] - df['completed'],
        name='Missed',
        marker_color='#F44336'
    ))
    
    fig.update_layout(
        title='Weekly Workout Completion',
        xaxis_title='Week',
        yaxis_title='Workouts',
        barmode='stack',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_macro_pie_chart(macros: Dict):
    """Render macro distribution pie chart."""
    labels = ['Protein', 'Carbs', 'Fats']
    values = [macros.get('protein', 30), macros.get('carbs', 40), macros.get('fats', 30)]
    colors = ['#FF6384', '#36A2EB', '#FFCE56']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker_colors=colors
    )])
    
    fig.update_layout(
        title='Macro Distribution (%)',
        annotations=[dict(text='Macros', x=0.5, y=0.5, font_size=16, showarrow=False)]
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_measurement_chart(measurement_data: List[Dict]):
    """Render body measurement trends chart."""
    if not measurement_data:
        st.info("📊 No measurement data available yet.")
        return
    
    df = pd.DataFrame(measurement_data)
    df['date'] = pd.to_datetime(df['date'])
    
    fig = go.Figure()
    
    measurements = ['waist', 'chest', 'biceps']
    colors = ['#E91E63', '#2196F3', '#4CAF50']
    
    for measure, color in zip(measurements, colors):
        if measure in df.columns and df[measure].notna().any():
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df[measure],
                name=measure.title(),
                line=dict(color=color),
                mode='lines+markers'
            ))
    
    fig.update_layout(
        title='Body Measurements Over Time',
        xaxis_title='Date',
        yaxis_title='Centimeters',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_progress_summary_cards(summary: Dict):
    """Render progress summary as metric cards."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Current Weight",
            value=f"{summary.get('current_weight', 0):.1f} kg",
            delta=f"{summary.get('weight_change', 0):.1f} kg"
        )
    
    with col2:
        st.metric(
            label="Workout Completion",
            value=f"{summary.get('completion_rate', 0):.0f}%"
        )
    
    with col3:
        st.metric(
            label="Avg Daily Calories",
            value=f"{summary.get('avg_daily_calories', 0):.0f}"
        )
    
    with col4:
        st.metric(
            label="Calorie Adherence",
            value=f"{summary.get('adherence_rate', 0):.0f}%"
        )


# ==================== CARD COMPONENTS ====================

def render_stats_cards(stats: Dict):
    """Render user statistics cards."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1rem; border-radius: 0.5rem; color: white; text-align: center;">
            <h4 style="margin: 0; font-size: 0.9rem;">BMI</h4>
            <h2 style="margin: 0.5rem 0; font-size: 1.8rem;">{stats.get('bmi', 0):.1f}</h2>
            <p style="margin: 0; font-size: 0.8rem;">{stats.get('bmi_category', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 1rem; border-radius: 0.5rem; color: white; text-align: center;">
            <h4 style="margin: 0; font-size: 0.9rem;">Daily Calories</h4>
            <h2 style="margin: 0.5rem 0; font-size: 1.8rem;">{stats.get('daily_calories', 0)}</h2>
            <p style="margin: 0; font-size: 0.8rem;">kcal/day</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 1rem; border-radius: 0.5rem; color: white; text-align: center;">
            <h4 style="margin: 0; font-size: 0.9rem;">BMR</h4>
            <h2 style="margin: 0.5rem 0; font-size: 1.8rem;">{stats.get('bmr', 0)}</h2>
            <p style="margin: 0; font-size: 0.8rem;">kcal/day</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
                    padding: 1rem; border-radius: 0.5rem; color: white; text-align: center;">
            <h4 style="margin: 0; font-size: 0.9rem;">TDEE</h4>
            <h2 style="margin: 0.5rem 0; font-size: 1.8rem;">{stats.get('tdee', 0)}</h2>
            <p style="margin: 0; font-size: 0.8rem;">kcal/day</p>
        </div>
        """, unsafe_allow_html=True)


def render_macro_cards(stats: Dict):
    """Render macronutrient cards."""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="background: #FF6384; padding: 1rem; border-radius: 0.5rem; 
                    color: white; text-align: center;">
            <h4 style="margin: 0;">🥩 Protein</h4>
            <h2 style="margin: 0.5rem 0;">{stats.get('protein_g', 0)}g</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: #36A2EB; padding: 1rem; border-radius: 0.5rem; 
                    color: white; text-align: center;">
            <h4 style="margin: 0;">🍚 Carbs</h4>
            <h2 style="margin: 0.5rem 0;">{stats.get('carbs_g', 0)}g</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: #FFCE56; padding: 1rem; border-radius: 0.5rem; 
                    color: #333; text-align: center;">
            <h4 style="margin: 0;">🥑 Fats</h4>
            <h2 style="margin: 0.5rem 0;">{stats.get('fats_g', 0)}g</h2>
        </div>
        """, unsafe_allow_html=True)


def render_insight_cards(insights: List[str], adjustments: List[str]):
    """Render insight and adjustment cards."""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💡 Insights")
        if insights:
            for insight in insights:
                st.info(insight)
        else:
            st.info("Start logging progress to see insights!")
    
    with col2:
        st.markdown("### 🔧 Recommended Adjustments")
        if adjustments:
            for adjustment in adjustments:
                st.warning(adjustment)
        else:
            st.success("Keep following your current plan!")


# ==================== FORM COMPONENTS ====================

def render_profile_form(existing_data: Optional[Dict] = None) -> Optional[Dict]:
    """Render user profile form and return data if submitted."""
    
    with st.form("profile_form", clear_on_submit=False):
        st.subheader("📋 Personal Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(
                "Full Name *",
                value=existing_data.get("name", "") if existing_data else "",
                placeholder="Enter your full name"
            )
            email = st.text_input(
                "Email *",
                value=existing_data.get("email", "") if existing_data else "",
                placeholder="your@email.com",
                disabled=existing_data is not None  # Can't change email after creation
            )
            age = st.number_input(
                "Age *",
                min_value=16,
                max_value=80,
                value=existing_data.get("age", 25) if existing_data else 25
            )
            gender = st.selectbox(
                "Gender *",
                options=["male", "female", "other"],
                index=["male", "female", "other"].index(
                    existing_data.get("gender", "male")
                ) if existing_data else 0
            )
        
        with col2:
            height = st.number_input(
                "Height (cm) *",
                min_value=100.0,
                max_value=250.0,
                value=float(existing_data.get("height_cm", 170.0)) if existing_data else 170.0,
                step=0.5
            )
            weight = st.number_input(
                "Weight (kg) *",
                min_value=30.0,
                max_value=300.0,
                value=float(existing_data.get("weight_kg", 70.0)) if existing_data else 70.0,
                step=0.5
            )
        
        st.markdown("---")
        st.subheader("🎯 Fitness Goals")
        
        col1, col2 = st.columns(2)
        
        # Goal options
        goal_options = ["lean", "muscle_gain", "fat_loss"]
        goal_labels = {
            "lean": "🏃 Get Lean & Toned",
            "muscle_gain": "💪 Build Muscle",
            "fat_loss": "🔥 Lose Fat"
        }
        
        # Activity options
        activity_options = ["sedentary", "lightly_active", "moderately_active", "very_active", "extremely_active"]
        activity_labels = {
            "sedentary": "🪑 Sedentary (little/no exercise)",
            "lightly_active": "🚶 Lightly Active (1-3 days/week)",
            "moderately_active": "🏃 Moderately Active (3-5 days/week)",
            "very_active": "🏋️ Very Active (6-7 days/week)",
            "extremely_active": "⚡ Extremely Active (athlete)"
        }
        
        with col1:
            current_goal = existing_data.get("fitness_goal", "lean") if existing_data else "lean"
            goal_index = goal_options.index(current_goal) if current_goal in goal_options else 0
            fitness_goal = st.selectbox(
                "Primary Goal *",
                options=goal_options,
                format_func=lambda x: goal_labels.get(x, x),
                index=goal_index
            )
            
            current_activity = existing_data.get("activity_level", "moderately_active") if existing_data else "moderately_active"
            activity_index = activity_options.index(current_activity) if current_activity in activity_options else 2
            activity_level = st.selectbox(
                "Activity Level *",
                options=activity_options,
                format_func=lambda x: activity_labels.get(x, x),
                index=activity_index
            )
        
        # Experience options
        exp_options = ["beginner", "intermediate", "advanced"]
        exp_labels = {
            "beginner": "🌱 Beginner (0-1 year)",
            "intermediate": "📈 Intermediate (1-3 years)",
            "advanced": "🏆 Advanced (3+ years)"
        }
        
        # Location options
        loc_options = ["home", "gym", "both"]
        loc_labels = {
            "home": "🏠 Home",
            "gym": "🏋️ Gym",
            "both": "🔄 Both"
        }
        
        with col2:
            current_exp = existing_data.get("experience_level", "beginner") if existing_data else "beginner"
            exp_index = exp_options.index(current_exp) if current_exp in exp_options else 0
            experience_level = st.selectbox(
                "Experience Level *",
                options=exp_options,
                format_func=lambda x: exp_labels.get(x, x),
                index=exp_index
            )
            
            current_loc = existing_data.get("workout_location", "gym") if existing_data else "gym"
            loc_index = loc_options.index(current_loc) if current_loc in loc_options else 1
            workout_location = st.selectbox(
                "Workout Location *",
                options=loc_options,
                format_func=lambda x: loc_labels.get(x, x),
                index=loc_index
            )
        
        workout_days = st.slider(
            "Workout Days per Week *",
            min_value=1,
            max_value=7,
            value=existing_data.get("workout_days_per_week", 4) if existing_data else 4
        )
        
        st.markdown("---")
        st.subheader("🥗 Dietary Preferences")
        
        # Diet options
        diet_options = ["indian_veg", "indian_non_veg", "vegan", "keto", "balanced"]
        diet_labels = {
            "indian_veg": "🥬 Indian Vegetarian",
            "indian_non_veg": "🍗 Indian Non-Vegetarian",
            "vegan": "🌿 Vegan",
            "keto": "🥑 Keto",
            "balanced": "⚖️ Balanced"
        }
        
        current_diet = existing_data.get("dietary_preference", "balanced") if existing_data else "balanced"
        diet_index = diet_options.index(current_diet) if current_diet in diet_options else 4
        dietary_preference = st.selectbox(
            "Dietary Preference *",
            options=diet_options,
            format_func=lambda x: diet_labels.get(x, x),
            index=diet_index
        )
        
        st.markdown("---")
        st.subheader("⚕️ Health Information (Optional)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            medical_conditions = st.text_area(
                "Medical Conditions",
                value=existing_data.get("medical_conditions", "") if existing_data else "",
                placeholder="E.g., diabetes, hypertension, back pain...",
                help="List any conditions that may affect exercise or diet",
                height=100
            )
        
        with col2:
            allergies = st.text_area(
                "Food Allergies",
                value=existing_data.get("allergies", "") if existing_data else "",
                placeholder="E.g., nuts, dairy, gluten...",
                help="List any food allergies or intolerances",
                height=100
            )
        
        st.markdown("---")
        
        # Submit button
        submit_label = "💾 Update Profile" if existing_data else "🚀 Create Profile"
        submitted = st.form_submit_button(submit_label, use_container_width=True, type="primary")
        
        if submitted:
            # Validation
            if not name.strip():
                st.error("❌ Please enter your name")
                return None
            
            if not existing_data and not email.strip():
                st.error("❌ Please enter your email")
                return None
            
            if not existing_data and "@" not in email:
                st.error("❌ Please enter a valid email address")
                return None
            
            # Return form data
            return {
                "name": name.strip(),
                "email": email.lower().strip() if not existing_data else existing_data.get("email"),
                "age": age,
                "gender": gender,
                "height_cm": height,
                "weight_kg": weight,
                "fitness_goal": fitness_goal,
                "activity_level": activity_level,
                "experience_level": experience_level,
                "workout_location": workout_location,
                "workout_days_per_week": workout_days,
                "dietary_preference": dietary_preference,
                "medical_conditions": medical_conditions.strip() if medical_conditions else None,
                "allergies": allergies.strip() if allergies else None
            }
    
    return None
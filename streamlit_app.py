import os
import re
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# -------------------------------
# Load Environment Variables
# -------------------------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ GEMINI_API_KEY not found in your .env file. Please add it and restart.")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Skoooliq AI Meal & Workout Planner", layout="wide")

st.title("🍎 Skoooliq AI Meal & Workout Planner")
st.markdown("Enter your details and goals to get a **personalized 7-day meal & workout plan** with daily calories.")

# User Inputs
col1, col2, col3 = st.columns(3)
with col1:
    age = st.number_input("Age", min_value=5, max_value=100, value=18)
    weight = st.number_input("Weight (kg)", min_value=20, max_value=200, value=65)
    diet_pref = st.selectbox("Diet Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])
with col2:
    height = st.number_input("Height (cm)", min_value=100, max_value=220, value=170)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    activity = st.selectbox("Activity Level", ["Low", "Moderate", "High"])
with col3:
    goal = st.selectbox("Goal", ["Weight Loss", "Weight Gain", "Maintain"])
    disease = st.text_input("Diseases/Conditions (comma separated)", "None")
    allergies = st.text_input("Allergies (comma separated)", "None")

# -------------------------------
# Generate Plan
# -------------------------------
if st.button("Generate 7-Day Plan"):
    with st.spinner("⏳ Generating your personalized plan..."):
        prompt = f"""
        You are a professional nutritionist and fitness coach.
        Generate a **7-day meal and workout plan** for:
        - Age: {age}
        - Gender: {gender}
        - Weight: {weight} kg
        - Height: {height} cm
        - Activity Level: {activity}
        - Health Condition(s): {disease}
        - Allergies: {allergies}
        - Diet Preference: {diet_pref}
        - Goal: {goal}

        Rules:
        1. Each day must include Breakfast, Lunch, Dinner, and Snack.
        2. Show calories for each meal and total daily calories.
        3. After the meal table, show the workout plan for the day.
        4. Use Markdown table format only.
        5. Do not skip any days, write all 7 days in full detail.

        Table Format:
        | Meal      | Food Description | Calories |
        |-----------|------------------|----------|
        """

        try:
            response = model.generate_content(prompt)
            st.success("✅ Plan Generated successfully!")

            # --- Split into Days correctly ---
            pattern = r"(Day \d[\s\S]*?)(?=Day \d|$)"
            matches = re.findall(pattern, response.text)

            # Tabs for each day
            days = [f"Day {i}" for i in range(1, 8)]
            tabs = st.tabs(days)

            for i, tab in enumerate(tabs, start=1):
                with tab:
                    st.markdown(f"## Day {i}")
                    if i-1 < len(matches):
                        day_text = matches[i-1]

                        # Show as markdown table
                        st.markdown(day_text, unsafe_allow_html=True)
                    else:
                        st.warning("⚠️ No plan generated for this day.")

        except Exception as e:
            st.error(f"⚠️ Error generating plan: {e}")

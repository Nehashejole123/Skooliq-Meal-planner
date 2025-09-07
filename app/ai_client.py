import streamlit as st
import pandas as pd
from mealplan_generator import generate_meal_plan  # this is your Gemini call wrapper

st.set_page_config(page_title="AI Meal Planner", layout="wide")

st.title("🥗 AI-Powered Meal Planner")
st.header("Step 3: Generate Meal Plan")

if st.button("Generate 7-Day Meal Plan"):
    with st.spinner("Generating meal plan using Gemini AI..."):
        plan = generate_meal_plan()

    if "error" in plan.get("plan", {}):
        st.error("⚠️ Failed to generate meal plan.")
        st.json(plan)  # fallback for debugging
    else:
        st.success("✅ Meal plan generated!")

        # Extract week plan
        week_plan = plan["plan"]["week_plan"]

        # Convert into DataFrame for nice display
        data = []
        for day, meals in week_plan.items():
            data.append({
                "Day": day,
                "Breakfast": meals.get("breakfast", ""),
                "Lunch": meals.get("lunch", ""),
                "Dinner": meals.get("dinner", ""),
                "Calories": meals.get("calories", "")
            })

        df = pd.DataFrame(data)

        # Show table
        st.dataframe(df, use_container_width=True)

        # Optional: Allow download as CSV
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Meal Plan as CSV",
            data=csv,
            file_name="meal_plan.csv",
            mime="text/csv"
        )


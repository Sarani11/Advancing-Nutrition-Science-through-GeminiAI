import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
import datetime

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("⚠️ GROQ_API_KEY not found. Please set it in your .env file.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

MODEL = "llama-3.3-70b-versatile"

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------

st.set_page_config(
    page_title="NutriGen - AI Nutrition Assistant",
    page_icon="🥗",
    layout="wide"
)

st.title("🥗 NutriGen")
st.subheader("AI-Powered Personalized Nutrition & Wellness Assistant")

# ---------------------------------------
# FUNCTION
# ---------------------------------------

def generate_response(prompt):
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a certified professional nutritionist and diet planning expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=1200
    )
    return completion.choices[0].message.content

# ---------------------------------------
# SIDEBAR
# ---------------------------------------

scenario = st.sidebar.radio(
    "Select Feature",
    [
        "Scenario 1: Tailored Meal Planning",
        "Scenario 2: Dynamic Nutritional Insights",
        "Scenario 3: Virtual Nutrition Coaching"
    ]
)

# ======================================
# SCENARIO 1: Tailored Meal Planning
# ======================================

if scenario == "Scenario 1: Tailored Meal Planning":

    st.header("📅 Personalized Weekly Meal Plan")

    col1, col2 = st.columns(2)

    with col1:
        restrictions = st.text_input("Dietary Restrictions / Allergies")
        health = st.text_input("Health Conditions")

    with col2:
        activity = st.selectbox(
            "Activity Level",
            ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"]
        )
        preference = st.text_input("Taste Preferences")

    if st.button("Generate Meal Plan"):

        prompt = f"""
        Create a detailed 7-day personalized meal plan.

        Dietary Restrictions: {restrictions}
        Health Conditions: {health}
        Activity Level: {activity}
        Taste Preferences: {preference}

        Include:
        - Breakfast, Lunch, Dinner
        - Nutritional breakdown
        - Grocery list
        """

        with st.spinner("Generating your personalized meal plan..."):
            result = generate_response(prompt)

        st.success("Your Customized Plan:")
        st.write(result)

# ======================================
# SCENARIO 2: Dynamic Nutritional Insights
# ======================================

elif scenario == "Scenario 2: Dynamic Nutritional Insights":

    st.header("🔍 Nutritional Breakdown")

    col1, col2 = st.columns(2)

    with col1:
        food_item = st.text_input("Enter Food Item Name")

    with col2:
        barcode = st.text_input("Or Enter Barcode Number")

    if "nutrition_log" not in st.session_state:
        st.session_state.nutrition_log = []

    if st.button("Analyze Nutrition"):

        item_to_analyze = food_item if food_item else f"Product with barcode {barcode}"

        prompt = f"""
        Provide detailed nutritional analysis for: {item_to_analyze}

        Include:

        1. Macronutrients:
           - Protein (grams)
           - Carbohydrates (grams)
           - Fats (grams)

        2. Micronutrients:
           - Vitamins
           - Minerals

        3. Total Estimated Calories

        4. Health Benefits

        5. Possible Health Risks (if consumed excessively)
        """

        with st.spinner("Analyzing nutritional content..."):
            result = generate_response(prompt)

        st.success("Detailed Nutritional Report:")
        st.write(result)

        st.session_state.nutrition_log.append({
            "item": item_to_analyze,
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        })

    if st.session_state.nutrition_log:
        st.markdown("### 📊 Nutrition Tracking History")
        for entry in st.session_state.nutrition_log:
            st.write(f"• {entry['item']} — {entry['time']}")

# ======================================
# SCENARIO 3: Virtual Nutrition Coaching
# ======================================

elif scenario == "Scenario 3: Virtual Nutrition Coaching":

    st.header("💬 Virtual Nutrition Coach")

    question = st.text_area("Ask your nutrition question")

    if st.button("Ask Coach"):

        prompt = f"""
        Act as a certified nutritionist.

        Answer this question in detail:
        {question}

        Provide scientific explanation and practical advice.
        """

        with st.spinner("Consulting your AI Coach..."):
            result = generate_response(prompt)

        st.success("Coach's Advice:")
        st.write(result)

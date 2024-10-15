import streamlit as st
import pandas as pd

st.title("Macro Nutrient Tracker")

# Define macro targets
st.header("Set Your Macro Targets")
target_period = st.selectbox("Select Target Period", ["Daily", "Weekly"])
protein_target = st.number_input("Protein Target (grams)", min_value=0.0, value=150.0)
carbs_target = st.number_input("Carbohydrates Target (grams)", min_value=0.0, value=200.0)
fats_target = st.number_input("Fats Target (grams)", min_value=0.0, value=70.0)

# Initialize session state
if 'meals' not in st.session_state:
    st.session_state['meals'] = []

# Meal logging
st.header("Log Your Meal")
protein_consumed = st.number_input("Protein Consumed (grams)", min_value=0.0, key='protein_consumed')
carbs_consumed = st.number_input("Carbohydrates Consumed (grams)", min_value=0.0, key='carbs_consumed')
fats_consumed = st.number_input("Fats Consumed (grams)", min_value=0.0, key='fats_consumed')

if st.button("Add Meal"):
    st.session_state['meals'].append({
        'protein': protein_consumed,
        'carbs': carbs_consumed,
        'fats': fats_consumed
    })
    st.session_state['protein_consumed'] = 0.0
    st.session_state['carbs_consumed'] = 0.0
    st.session_state['fats_consumed'] = 0.0

# Calculate totals and remaining macros
total_protein_consumed = sum(meal['protein'] for meal in st.session_state['meals'])
total_carbs_consumed = sum(meal['carbs'] for meal in st.session_state['meals'])
total_fats_consumed = sum(meal['fats'] for meal in st.session_state['meals'])

protein_remaining = max(protein_target - total_protein_consumed, 0)
carbs_remaining = max(carbs_target - total_carbs_consumed, 0)
fats_remaining = max(fats_target - total_fats_consumed, 0)

# Display remaining macros
st.header("Remaining Macros")
st.write(f"**Protein Remaining:** {protein_remaining:.2f} grams")
st.write(f"**Carbohydrates Remaining:** {carbs_remaining:.2f} grams")
st.write(f"**Fats Remaining:** {fats_remaining:.2f} grams")

# Divide remaining macros among remaining meals
meals_left = st.number_input("Number of Meals Remaining", min_value=1, value=3)
protein_per_meal = protein_remaining / meals_left
carbs_per_meal = carbs_remaining / meals_left
fats_per_meal = fats_remaining / meals_left

st.header("Macros Needed Per Remaining Meal")
st.write(f"**Protein per Meal:** {protein_per_meal:.2f} grams")
st.write(f"**Carbohydrates per Meal:** {carbs_per_meal:.2f} grams")
st.write(f"**Fats per Meal:** {fats_per_meal:.2f} grams")

# Display meal history
st.header("Meal History")
if st.session_state['meals']:
    meals_df = pd.DataFrame(st.session_state['meals'])
    st.table(meals_df)
else:
    st.write("No meals logged yet.")

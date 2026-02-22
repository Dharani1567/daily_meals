import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# ---- Google Auth ----
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "credentials.json",  # your JSON file
    scopes=scope
)

client = gspread.authorize(creds)

sheet = client.open("MealsTracker").sheet1  # Sheet name


# ---- UI ----
st.title("Meals Entry")

meal_type = st.selectbox(
    "Type of Meal",
    ["Breakfast", "Lunch", "Dinner", "Snacks"]
)

cost = st.number_input("Cost", min_value=0)

num_meals = st.number_input("Number of Meals", min_value=1)

company = st.text_input("Company")

if st.button("Save Entry"):

    date = datetime.now().strftime("%Y-%m-%d")

    row = [meal_type, cost, num_meals, company, date]

    sheet.append_row(row)

    st.success("Entry Saved ✅")
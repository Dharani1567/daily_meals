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
    "credentials.json",
    scopes=scope
)

client = gspread.authorize(creds)

sheet = client.open("MealsTracker").sheet1

# ---- AUTO CREATE TABLE ----
existing_data = sheet.get_all_values()

if not existing_data:
    sheet.append_row([
        "Type of Meal",
        "Cost of One Plate",
        "Total Plates",
        "Total Cost",
        "Company",
        "Date"
    ])

# ---- UI ----
st.title("Meals Entry")

meal_type = st.text_input("Type of Meal")

one_plate_cost = st.number_input("Cost of One Plate", min_value=0)

total_plates = st.number_input("Total Plates", min_value=1)

company = st.text_input("Company")

date = st.date_input("Date")

# ---- Auto Calculation ----
total_cost = one_plate_cost * total_plates

st.write("### Total Cost:", total_cost)

# ---- Save Button ----
if st.button("Save Entry"):

    if meal_type.strip() == "":
        st.error("Meal Type required")
    elif one_plate_cost <= 0:
        st.error("Cost must be greater than zero")
    elif company.strip() == "":
        st.error("Company required")
    else:
        row = [
            meal_type,
            one_plate_cost,
            total_plates,
            total_cost,
            company,
            str(date)
        ]

        sheet.append_row(row)

        st.success("Entry Saved ✅")
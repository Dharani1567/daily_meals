import streamlit as st
import sqlite3
from datetime import date
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- DATABASE ---------------- #

conn = sqlite3.connect("meals.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS meals (
    entry_date TEXT,
    company TEXT,
    meals INTEGER,
    cost REAL
)
""")
conn.commit()

def save_to_db(entry_date, company, meals, cost):
    cursor.execute(
        "INSERT INTO meals VALUES (?, ?, ?, ?)",
        (entry_date, company, meals, cost)
    )
    conn.commit()

def get_month_data(company, month):
    cursor.execute("""
        SELECT * FROM meals
        WHERE company = ? AND entry_date LIKE ?
    """, (company, f"{month}%"))
    return cursor.fetchall()

# ---------------- PDF ---------------- #

def generate_pdf(company, month):
    data = get_month_data(company, month)

    file_name = f"{company}_{month}_report.pdf"
    pdf = SimpleDocTemplate(file_name, pagesize=A4)

    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(f"<b>Monthly Report — {company}</b>", styles['Title']))
    elements.append(Spacer(1, 20))

    total_meals = sum(row[2] for row in data)
    total_cost = sum(row[3] for row in data)

    elements.append(Paragraph(f"Total Meals: {total_meals}", styles['Normal']))
    elements.append(Paragraph(f"Total Cost: ₹ {total_cost:.2f}", styles['Normal']))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("<b>Daily Breakdown</b>", styles['Heading2']))
    elements.append(Spacer(1, 10))

    for row in data:
        elements.append(
            Paragraph(
                f"{row[0]} — {row[2]} meals — ₹ {row[3]:.2f}",
                styles['Normal']
            )
        )

    pdf.build(elements)
    return file_name

# ---------------- UI ---------------- #

st.title("🍽 Daily Meal Entry")

companies = [
    "Company A",
    "Company B",
    "Company C"
]

company = st.selectbox("Select Company", companies)

meals = st.number_input("Meals Count", min_value=0)
cost = st.number_input("Total Cost (₹)", min_value=0.0)

if st.button("Submit ✅"):
    today = str(date.today())
    save_to_db(today, company, meals, cost)
    st.success("Saved Successfully ✅")

st.divider()

st.title("📄 Monthly Report")

report_company = st.selectbox("Company", companies, key="report")

month = st.text_input("Enter Month (YYYY-MM)", "2026-02")

if st.button("Generate PDF 📥"):
    file_name = generate_pdf(report_company, month)

    with open(file_name, "rb") as f:
        st.download_button("Download Report", f, file_name=file_name)
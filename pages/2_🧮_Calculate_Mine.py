import streamlit as st
from lib.inflation import compute_personal_inflation, CATEGORY_ORDER, load_cpi_data

st.set_page_config(page_title="Calculate Mine — Inflation Tracker", page_icon="🧮", layout="wide")
st.title("What's your personal inflation rate?")
st.caption("Enter your average monthly spend (₹) for each category. We compute your weighted personal rate using MOSPI's official CPI index changes.")

CATEGORY_META = {
    "food_beverages": ("Food & beverages", "Cereals, pulses, vegetables, milk, oils, spices", 9000, 40000),
    "housing": ("Housing", "Rent, house maintenance", 12000, 60000),
    "fuel_light": ("Fuel & light", "LPG, electricity, kerosene", 2500, 15000),
    "clothing": ("Clothing", "Garments, footwear, bedding", 1500, 10000),
    "transport": ("Transport", "Petrol, auto/bus/train, airfare", 3500, 20000),
    "healthcare": ("Healthcare", "Medicines, doctor/hospital fees", 2000, 15000),
    "education": ("Education", "Tuition, books, coaching", 3000, 20000),
    "misc": ("Miscellaneous", "Personal care, recreation, OTT, insurance", 4000, 20000),
}

left, right = st.columns([1.2, 0.8])

with left:
    st.subheader("Your monthly spend")
    spend = {}
    for key in CATEGORY_ORDER:
        label, hint, default, max_val = CATEGORY_META[key]
        spend[key] = st.slider(f"{label} — {hint}", min_value=0, max_value=max_val, value=default, step=100, key=key)

    st.write("")
    c1, c2 = st.columns(2)
    period = c1.selectbox("Period", ["3 months", "6 months", "1 year", "3 years"], index=2)
    area = c2.selectbox("Compare against", ["Urban", "Rural"])

result = compute_personal_inflation(spend, period, area)

with right:
    st.subheader("Your result")
    st.metric("Your personal inflation rate", f"{result['personal_rate']}%")
    st.metric(f"National CPI ({area}, {period})", f"{result['national_rate']}%")

    diff = result["personal_rate"] - result["national_rate"]
    if diff > 0:
        st.warning(f"You're experiencing inflation **{abs(diff):.1f} points higher** than the national average.")
    elif diff < 0:
        st.success(f"You're experiencing inflation **{abs(diff):.1f} points lower** than the national average.")
    else:
        st.info("Your rate matches the national average.")

    st.write("")
    st.markdown("**Top contributors**")
    for c in result["contributions"][:5]:
        st.write(f"{c['label']} — {c['weight']}% of spend → {'+' if c['cpi_pct_change'] >= 0 else ''}{c['cpi_pct_change']}% CPI change")
import streamlit as st

st.set_page_config(page_title="Personal Inflation Tracker — India", page_icon="₹", layout="wide")

# ---------- Custom CSS matching brand palette ----------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    h1, h2, h3 { font-family: 'Playfair Display', serif !important; }
    .hero-box {
        background: #1a3a2a;
        color: #F5F0E8;
        padding: 60px 40px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 30px;
    }
    .hero-box h1 { color: #F5F0E8; font-size: 2.6rem; }
    .hero-box p { color: #7ec99a; font-size: 1.1rem; }
    .stat-card {
        background: #E8E0D0;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .stat-card .num { font-family: 'Playfair Display', serif; font-size: 1.8rem; color: #2d7a4f; }
</style>
""", unsafe_allow_html=True)

# ---------- Hero ----------
st.markdown("""
<div class="hero-box">
    <h1>What does inflation actually cost you?</h1>
    <p>Enter what you actually spend in rupees each month, and see your own
    personal inflation rate against India's official CPI — urban or rural.</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="stat-card"><div class="num">39%</div>Food & beverages carry the largest weight in India\'s CPI basket (MOSPI, 2012=100)</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="stat-card"><div class="num">↑ Sharp</div>Fuel & light shows the sharpest short-term spikes, driven by LPG price revisions</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="stat-card"><div class="num">2012=100</div>MOSPI\'s official CPI base year — every index value is relative to this</div>', unsafe_allow_html=True)

st.write("")
st.subheader("How it works")
c1, c2, c3 = st.columns(3)
c1.markdown("**1. Enter your spend**\n\nMonthly ₹ spend across 8 official CPI categories")
c2.markdown("**2. We apply official CPI change**\n\nEach category weighted by real MOSPI index movement")
c3.markdown("**3. See your rate**\n\nCompared instantly against the national CPI")

st.info("👈 Use the sidebar to open **Trends** (see CPI charts) or **Calculate Mine** (get your personal rate).")

st.caption("Data sources: MOSPI · RBI DBIE · data.gov.in — India CPI base year 2012 = 100")
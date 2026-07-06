import streamlit as st
import plotly.graph_objects as go
from lib.inflation import (
    compute_personal_inflation,
    load_cpi_data,
    CATEGORY_ORDER,
    pct_change,
)

st.set_page_config(
    page_title="Personal Inflation Tracker — India",
    page_icon="₹",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# GLOBAL CSS — hides sidebar, sticky nav, cards, spacing
# =========================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    h1, h2, h3, h4 { font-family: 'Playfair Display', serif !important; }

    /* ---------- Hide Streamlit sidebar & its toggle completely ---------- */
    section[data-testid="stSidebar"] { display: none !important; }
    div[data-testid="collapsedControl"] { display: none !important; }
    button[kind="header"] { display: none !important; }

    /* ---------- Hide default Streamlit header/footer chrome ---------- */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent; }

    /* ---------- Widen content area ---------- */
    .main .block-container {
        max-width: 1300px;
        padding-top: 90px;
        padding-bottom: 60px;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
    }

    /* ---------- Sticky top navigation ---------- */
    .top-nav {
        position: fixed;
        top: 0; left: 0; right: 0;
        z-index: 999;
        background: #1a3a2a;
        padding: 14px 40px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 12px rgba(0,0,0,0.15);
    }
    .top-nav .brand {
        color: #F5F0E8;
        font-family: 'Playfair Display', serif;
        font-size: 1.15rem;
        font-weight: 700;
        text-decoration: none;
        white-space: nowrap;
    }
    .top-nav .brand span { color: #7ec99a; }
    .nav-links {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
    }
    .nav-links a {
        color: #F5F0E8;
        text-decoration: none;
        font-size: 0.92rem;
        font-weight: 600;
        padding: 9px 20px;
        border-radius: 999px;
        transition: background 0.2s ease, color 0.2s ease;
        opacity: 0.85;
    }
    .nav-links a:hover { opacity: 1; background: rgba(126,201,154,0.15); }
    .nav-links a.active {
        background: #2d7a4f;
        color: #ffffff;
        opacity: 1;
    }

    /* ---------- Generic card ---------- */
    .card {
        background: #ffffff;
        border: 1px solid #E8E0D0;
        border-radius: 18px;
        padding: 28px;
        box-shadow: 0 2px 10px rgba(26,58,42,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 24px;
    }
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 24px rgba(26,58,42,0.12);
    }

    /* ---------- Hero ---------- */
    .hero-box {
        background: linear-gradient(135deg, #1a3a2a 0%, #234f38 100%);
        color: #F5F0E8;
        padding: 70px 50px;
        border-radius: 22px;
        text-align: center;
        margin-bottom: 40px;
    }
    .hero-box h1 {
        color: #F5F0E8;
        font-size: 2.8rem;
        margin-bottom: 16px;
        line-height: 1.15;
    }
    .hero-box p {
        color: #cfe9d9;
        font-size: 1.15rem;
        max-width: 620px;
        margin: 0 auto;
    }
    .cta-row {
        display: flex;
        justify-content: center;
        gap: 16px;
        margin-top: 34px;
        flex-wrap: wrap;
    }
    .cta-btn {
        display: inline-block;
        padding: 14px 30px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.98rem;
        text-decoration: none;
        transition: transform 0.2s ease, background 0.2s ease;
    }
    .cta-primary { background: #2d7a4f; color: #ffffff; }
    .cta-primary:hover { background: #7ec99a; color: #1a3a2a; transform: translateY(-2px); }
    .cta-secondary { background: transparent; color: #F5F0E8; border: 1.5px solid #7ec99a; }
    .cta-secondary:hover { background: rgba(126,201,154,0.15); transform: translateY(-2px); }

    /* ---------- Stat cards ---------- */
    .stat-card {
        background: #E8E0D0;
        border-radius: 18px;
        padding: 28px 24px;
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
    }
    .stat-card:hover { transform: translateY(-4px); box-shadow: 0 10px 24px rgba(26,58,42,0.1); }
    .stat-card .icon { font-size: 2rem; margin-bottom: 10px; }
    .stat-card .num { font-family: 'Playfair Display', serif; font-size: 1.9rem; color: #2d7a4f; margin-bottom: 6px; }
    .stat-card .desc { font-size: 0.88rem; color: #3a3a30; }

    /* ---------- Section spacing ---------- */
    .section-block { margin-top: 56px; margin-bottom: 24px; }
    .section-eyebrow {
        font-size: 0.8rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #2d7a4f;
        font-weight: 700;
        margin-bottom: 6px;
    }

    /* ---------- Result card (Calculator page) ---------- */
    .result-card {
        background: linear-gradient(135deg, #1a3a2a 0%, #204a35 100%);
        color: #F5F0E8;
        border-radius: 22px;
        padding: 36px 32px;
        box-shadow: 0 8px 28px rgba(26,58,42,0.25);
    }
    .result-card .rate-label {
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #7ec99a;
        font-weight: 700;
    }
    .result-card .rate-value {
        font-family: 'Playfair Display', serif;
        font-size: 3.4rem;
        margin: 6px 0 22px;
        color: #ffffff;
    }
    .result-card .sub-metric {
        display: flex;
        justify-content: space-between;
        font-size: 0.92rem;
        margin-bottom: 4px;
        color: #e6f2ea;
    }
    .result-card .sub-metric b { color: #ffffff; }
    .bar-track {
        background: rgba(255,255,255,0.15);
        border-radius: 8px;
        height: 10px;
        margin-bottom: 18px;
        overflow: hidden;
    }
    .bar-fill { height: 100%; border-radius: 8px; }
    .result-card .comparison-note {
        background: rgba(126,201,154,0.15);
        border-left: 3px solid #7ec99a;
        padding: 12px 16px;
        border-radius: 0 10px 10px 0;
        font-size: 0.9rem;
        margin: 18px 0;
    }
    .contrib-title {
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #7ec99a;
        font-weight: 700;
        margin: 22px 0 12px;
        border-top: 1px solid rgba(255,255,255,0.15);
        padding-top: 18px;
    }
    .contrib-item {
        display: flex;
        justify-content: space-between;
        font-size: 0.88rem;
        padding: 7px 0;
        color: #e6f2ea;
    }

    /* ---------- Info / methodology card ---------- */
    .info-card {
        background: #2d7a4f;
        color: #F5F0E8;
        border-radius: 20px;
        padding: 34px 32px;
        margin: 20px 0 32px;
    }
    .info-card h3 { color: #ffffff; margin-bottom: 14px; }
    .info-card p { color: #e6f2ea; font-size: 0.96rem; }
    .formula-block {
        background: rgba(26,58,42,0.55);
        color: #d9f2e2;
        font-family: 'Inter', monospace;
        padding: 16px 20px;
        border-radius: 12px;
        font-size: 0.95rem;
        margin: 16px 0;
        overflow-x: auto;
        border-left: 4px solid #7ec99a;
    }

    /* ---------- Source cards ---------- */
    .source-card {
        background: #ffffff;
        border: 1px solid #E8E0D0;
        border-radius: 18px;
        padding: 28px;
        height: 100%;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .source-card:hover { transform: translateY(-4px); box-shadow: 0 10px 24px rgba(26,58,42,0.1); }
    .source-card h3 { margin-bottom: 10px; font-size: 1.1rem; }
    .source-card p { color: #4a4a3d; font-size: 0.9rem; margin-bottom: 18px; }
    .learn-more {
        display: inline-block;
        background: #2d7a4f;
        color: #ffffff !important;
        padding: 9px 20px;
        border-radius: 999px;
        text-decoration: none;
        font-size: 0.85rem;
        font-weight: 600;
        transition: background 0.2s ease;
    }
    .learn-more:hover { background: #1a3a2a; }

    /* ---------- Responsive ---------- */
    @media (max-width: 900px) {
        .top-nav { flex-direction: column; gap: 10px; padding: 12px 20px; }
        .main .block-container { padding-top: 140px; padding-left: 1.2rem; padding-right: 1.2rem; }
        .hero-box { padding: 46px 24px; }
        .hero-box h1 { font-size: 2rem; }
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# ROUTING (query-param based, no sidebar needed)
# =========================================================
PAGES = ["Home", "Calculator", "Trends", "Sources"]
current_page = st.query_params.get("page", "Home")
if current_page not in PAGES:
    current_page = "Home"

nav_html = '<div class="top-nav"><a class="brand" href="?page=Home">₹ <span>Personal Inflation Tracker</span></a><div class="nav-links">'
for p in PAGES:
    active_class = "active" if p == current_page else ""
    nav_html += f'<a href="?page={p}" class="{active_class}">{p}</a>'
nav_html += '</div></div>'
st.markdown(nav_html, unsafe_allow_html=True)


# =========================================================
# PAGE: HOME
# =========================================================
def render_home():
    st.markdown("""
    <div class="hero-box">
        <h1>What does inflation actually cost you?</h1>
        <p>Enter what you actually spend in rupees each month, and see your own
        personal inflation rate against India's official CPI — urban or rural.</p>
        <div class="cta-row">
            <a href="?page=Calculator" class="cta-btn cta-primary">Calculate My Inflation</a>
            <a href="?page=Trends" class="cta-btn cta-secondary">View Trends</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="icon">🍽️</div>
            <div class="num">39%</div>
            <div class="desc">Food & beverages carry the largest weight in India's CPI basket (MOSPI, 2012=100)</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="icon">⛽</div>
            <div class="num">↑ Sharp</div>
            <div class="desc">Fuel & light shows the sharpest short-term spikes, driven by LPG price revisions</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="icon">📊</div>
            <div class="num">2012=100</div>
            <div class="desc">MOSPI's official CPI base year — every index value is relative to this</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-block"><div class="section-eyebrow">How it works</div></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        st.markdown('<div class="card"><b>1. Enter your spend</b><br><br>Monthly ₹ spend across 8 official CPI categories</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card"><b>2. We apply official CPI change</b><br><br>Each category weighted by real MOSPI index movement</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="card"><b>3. See your rate</b><br><br>Compared instantly against the national CPI</div>', unsafe_allow_html=True)

    st.caption("Data sources: MOSPI · RBI DBIE · data.gov.in — India CPI base year 2012 = 100")


# =========================================================
# PAGE: TRENDS
# =========================================================
def render_trends():
    st.title("India CPI — How prices have moved")
    st.caption("Consumer Price Index data, base year 2012 = 100, sourced from MOSPI and cross-referenced against RBI DBIE.")

    data = load_cpi_data()

    area = st.radio("Area", ["Urban", "Rural"], horizontal=True)
    field = "index_urban" if area == "Urban" else "index_rural"

    st.markdown('<div class="section-block"><div class="section-eyebrow">Headline CPI</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Headline CPI, last 36 months")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data["months"], y=data["headline"][field],
        mode="lines", line=dict(color="#2d7a4f", width=3),
        fill="tozeroy", fillcolor="rgba(45,122,79,0.08)",
        name=f"Headline CPI ({area})"
    ))
    fig.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        yaxis=dict(gridcolor="#E8E0D0"), xaxis=dict(showgrid=False),
        height=380, margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.info("Notable move: food & beverages have historically spiked in this window, consistent with post-pandemic food price surges and periodic LPG revisions.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-block"><div class="section-eyebrow">Category breakdown</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Category breakdown")
    period_label = st.select_slider("Period", options=["3 months", "6 months", "1 year", "3 years"], value="1 year")
    months_map = {"3 months": 3, "6 months": 6, "1 year": 12, "3 years": 36}
    months_back = months_map[period_label]

    labels, changes = [], []
    for key in CATEGORY_ORDER:
        series = data["categories"][key][field]
        base = series[max(0, len(series) - 1 - months_back)]
        current = series[-1]
        labels.append(data["categories"][key]["label"])
        changes.append(round(pct_change(base, current), 2))

    colors = ["#2d7a4f" if v >= 0 else "#7ec99a" for v in changes]
    fig2 = go.Figure(go.Bar(x=labels, y=changes, marker_color=colors))
    fig2.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        yaxis=dict(gridcolor="#E8E0D0", ticksuffix="%"),
        height=380, margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# PAGE: CALCULATOR
# =========================================================
CATEGORY_META = {
    "food_beverages": ("Food & beverages", "Cereals, pulses, vegetables, milk, oils, spices", 9000),
    "housing": ("Housing", "Rent, house maintenance", 12000),
    "fuel_light": ("Fuel & light", "LPG, electricity, kerosene", 2500),
    "clothing": ("Clothing", "Garments, footwear, bedding", 1500),
    "transport": ("Transport", "Petrol, auto/bus/train, airfare", 3500),
    "healthcare": ("Healthcare", "Medicines, doctor/hospital fees", 2000),
    "education": ("Education", "Tuition, books, coaching", 3000),
    "misc": ("Miscellaneous", "Personal care, recreation, OTT, insurance", 4000),
}

def render_calculator():
    st.title("What's your personal inflation rate?")
    st.caption("Enter your average monthly spend (₹) for each category. We compute your weighted personal rate using MOSPI's official CPI index changes.")

    left, right = st.columns([1.2, 0.8], gap="large")

    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Your monthly spend")
        spend = {}
        for key in CATEGORY_ORDER:
            label, hint, default = CATEGORY_META[key]
            spend[key] = st.number_input(
                f"{label} — {hint} (₹ per month)",
                min_value=0, value=default, step=100, key=key
            )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        period = c1.selectbox("Period", ["3 months", "6 months", "1 year", "3 years"], index=2)
        area = c2.selectbox("Compare against", ["Urban", "Rural"])
        st.markdown('</div>', unsafe_allow_html=True)

    result = compute_personal_inflation(spend, period, area)

    with right:
        max_abs = max(abs(result["personal_rate"]), abs(result["national_rate"]), 1)
        you_width = min(100, (abs(result["personal_rate"]) / max_abs) * 100)
        nat_width = min(100, (abs(result["national_rate"]) / max_abs) * 100)

        diff = result["personal_rate"] - result["national_rate"]
        if diff > 0:
            comparison_text = f"You're experiencing inflation <b>{abs(diff):.1f} points higher</b> than the national average."
        elif diff < 0:
            comparison_text = f"You're experiencing inflation <b>{abs(diff):.1f} points lower</b> than the national average."
        else:
            comparison_text = "Your rate matches the national average."

        contrib_html = ""
        if result["contributions"]:
            for c in result["contributions"][:5]:
                sign = "+" if c["cpi_pct_change"] >= 0 else ""
                contrib_html += f'<div class="contrib-item"><span>{c["label"]} <span style="opacity:0.6">({c["weight"]}% of spend)</span></span><span><b>{sign}{c["cpi_pct_change"]}%</b></span></div>'
        else:
            contrib_html = '<div class="contrib-item" style="opacity:0.6;">Enter your spend to see what\'s driving your rate.</div>'

        st.markdown(f"""
        <div class="result-card">
            <div class="rate-label">Your personal inflation rate</div>
            <div class="rate-value">{result['personal_rate']}%</div>

            <div class="sub-metric"><span>You</span><b>{result['personal_rate']}%</b></div>
            <div class="bar-track"><div class="bar-fill" style="width:{you_width}%; background:#7ec99a;"></div></div>

            <div class="sub-metric"><span>National CPI ({area})</span><b>{result['national_rate']}%</b></div>
            <div class="bar-track"><div class="bar-fill" style="width:{nat_width}%; background:#ffffff;"></div></div>

            <div class="comparison-note">{comparison_text}</div>

            <div class="contrib-title">Top contributors</div>
            {contrib_html}
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# PAGE: SOURCES
# =========================================================
def render_sources():
    st.title("Where this data comes from")
    st.caption("Every figure on this site traces back to Indian government data.")

    st.markdown('<div class="section-block"></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        st.markdown("""
        <div class="source-card">
            <h3>MOSPI</h3>
            <p>Ministry of Statistics & Programme Implementation. Official source for India's CPI, released monthly for all-India and state level, rural and urban.</p>
            <a class="learn-more" href="https://mospi.gov.in" target="_blank">Learn More →</a>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="source-card">
            <h3>RBI DBIE</h3>
            <p>Reserve Bank of India's Database on Indian Economy. Used here as a cross-reference for long historical CPI and WPI series.</p>
            <a class="learn-more" href="https://dbie.rbi.org.in" target="_blank">Learn More →</a>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="source-card">
            <h3>data.gov.in</h3>
            <p>The Open Government Data Platform. Aggregates MOSPI datasets behind a clean REST API.</p>
            <a class="learn-more" href="https://data.gov.in/catalog/consumer-price-index" target="_blank">Learn More →</a>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-block"><div class="section-eyebrow">Methodology</div></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-card">
        <h3>How we calculate your inflation</h3>
        <p>For every category you enter a monthly spend for, we work out its share of your total spend, then multiply that share by the official CPI percentage change for that category over your chosen period. Summing every category gives your personal rate.</p>
        <div class="formula-block">personal_rate = Σ (spend_category ÷ total_spend) × cpi_%_change_category</div>
        <p>All index values use MOSPI's current CPI series, base year <b>2012 = 100</b>.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-block"><div class="section-eyebrow">FAQ</div></div>', unsafe_allow_html=True)
    with st.expander("Why does my rate differ from the headline number in the news?"):
        st.write("The headline CPI reflects an average household's basket. Your own spending mix is almost never identical to that average, so your real experience of inflation is usually higher or lower than the headline.")
    with st.expander("What's the difference between urban and rural CPI?"):
        st.write("MOSPI publishes separate CPI series for urban and rural India because consumption patterns differ — for example, housing carries zero weight in the rural index.")
    with st.expander("Is this official government data?"):
        st.write("The category-level and headline index values are structured to match MOSPI's published CPI methodology. This build ships with a static fallback dataset — connect it to the data.gov.in API for live figures.")


# =========================================================
# RENDER CURRENT PAGE
# =========================================================
if current_page == "Home":
    render_home()
elif current_page == "Calculator":
    render_calculator()
elif current_page == "Trends":
    render_trends()
elif current_page == "Sources":
    render_sources()
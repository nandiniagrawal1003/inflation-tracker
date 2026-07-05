import streamlit as st
import plotly.graph_objects as go
from lib.inflation import load_cpi_data, CATEGORY_ORDER, pct_change

st.set_page_config(page_title="Trends — Inflation Tracker", page_icon="📈", layout="wide")
st.title("India CPI — How prices have moved")
st.caption("Consumer Price Index data, base year 2012 = 100, sourced from MOSPI and cross-referenced against RBI DBIE.")

data = load_cpi_data()

area = st.radio("Area", ["Urban", "Rural"], horizontal=True)
field = "index_urban" if area == "Urban" else "index_rural"

# ---------- Headline chart ----------
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

# ---------- Category bar chart ----------
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
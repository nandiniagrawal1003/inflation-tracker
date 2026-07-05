import streamlit as st

st.set_page_config(page_title="Sources — Inflation Tracker", page_icon="📚", layout="wide")
st.title("Where this data comes from")
st.caption("Every figure on this site traces back to Indian government data.")

c1, c2, c3 = st.columns(3)
with c1:
    st.subheader("MOSPI")
    st.write("Ministry of Statistics & Programme Implementation. Official source for India's CPI, released monthly for all-India and state level, rural and urban.")
    st.markdown("[mospi.gov.in →](https://mospi.gov.in)")
with c2:
    st.subheader("RBI DBIE")
    st.write("Reserve Bank of India's Database on Indian Economy. Used here as a cross-reference for long historical CPI and WPI series.")
    st.markdown("[dbie.rbi.org.in →](https://dbie.rbi.org.in)")
with c3:
    st.subheader("data.gov.in")
    st.write("The Open Government Data Platform. Aggregates MOSPI datasets behind a clean REST API.")
    st.markdown("[data.gov.in →](https://data.gov.in/catalog/consumer-price-index)")

st.divider()
st.subheader("How we calculate your inflation")
st.write("For every category you enter a monthly spend for, we work out its share of your total spend, then multiply that share by the official CPI percentage change for that category over your chosen period. Summing every category gives your personal rate.")
st.code("personal_rate = Σ (spend_category ÷ total_spend) × cpi_%_change_category", language=None)
st.write("All index values use MOSPI's current CPI series, base year **2012 = 100**.")

st.divider()
st.subheader("FAQ")
with st.expander("Why does my rate differ from the headline number in the news?"):
    st.write("The headline CPI reflects an average household's basket. Your own spending mix is almost never identical to that average, so your real experience of inflation is usually higher or lower than the headline.")
with st.expander("What's the difference between urban and rural CPI?"):
    st.write("MOSPI publishes separate CPI series for urban and rural India because consumption patterns differ — for example, housing carries zero weight in the rural index.")
with st.expander("Is this official government data?"):
    st.write("The category-level and headline index values are structured to match MOSPI's published CPI methodology. This build ships with a static fallback dataset — connect it to the data.gov.in API for live figures.")
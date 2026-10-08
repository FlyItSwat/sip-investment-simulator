"""Interactive SIP and lump-sum investment simulator."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from calculator import project, inr

st.set_page_config(page_title="SIP Investment Simulator", page_icon="📈", layout="wide")
st.title("SIP & Compound Interest Simulator")
st.caption("Explore SIPs, lump-sum investments, annual SIP step-ups, and inflation-adjusted wealth.")
with st.sidebar:
    st.header("Investment assumptions")
    monthly = st.number_input("Monthly SIP (₹)", min_value=0.0, max_value=10000000.0,
                              value=5000.0, step=500.0)
    initial = st.number_input("Initial lump sum (₹)", min_value=0.0, max_value=100000000.0,
                             value=0.0, step=1000.0)
    years = st.slider("Investment duration (years)", 1, 60, 20)
    annual_return = st.slider("Expected annual return (%)", -20.0, 30.0, 12.0, 0.5)
    inflation = st.slider("Annual inflation assumption (%)", 0.0, 15.0, 6.0, 0.5)
    step_up = st.slider("Annual SIP increase (%)", 0.0, 30.0, 0.0, 1.0)

p = project(monthly, initial, years, annual_return, inflation, step_up)
gain = p.nominal[-1] - p.invested[-1]
a, b, c, d = st.columns(4)
a.metric("Total invested", inr(p.invested[-1]))
b.metric("Projected value", inr(p.nominal[-1]))
c.metric("Investment gain", inr(gain))
d.metric("Today's purchasing power", inr(p.real[-1]))
df = pd.DataFrame({"Year": [m / 12 for m in p.months],
                   "Invested": p.invested,
                   "Nominal value": p.nominal,
                   "Inflation-adjusted value": p.real})
fig = go.Figure()
for label in ["Invested", "Nominal value", "Inflation-adjusted value"]:
    fig.add_trace(go.Scatter(x=df["Year"], y=df[label], mode="lines",
                             name=label, hovertemplate="Year %{x:.1f}<br>₹%{y:,.0f}<extra></extra>"))
fig.update_layout(title="Investment growth over time", xaxis_title="Years",
                  yaxis_title="Value (₹)", hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)
st.subheader("Annual snapshot")
annual = df.iloc[12::12].copy()
annual["Year"] = annual["Year"].astype(int)
st.dataframe(annual.style.format({"Invested": "₹{:,.0f}",
                                  "Nominal value": "₹{:,.0f}",
                                  "Inflation-adjusted value": "₹{:,.0f}"}),
             use_container_width=True, hide_index=True)
st.download_button("Download monthly projections (CSV)",
                   df.to_csv(index=False).encode("utf-8"),
                   "sip_projection.csv", "text/csv")
st.info("Educational illustration, not investment advice. Constant returns are assumed; "
        "real markets fluctuate. Returns, taxes, fees, and actual inflation may differ. "
        "SIP contributions are made at each month-end. Rates are nominal and divided by 12 "
        "for monthly calculations; inflation-adjusted values are in today's rupees.")

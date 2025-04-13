import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import os
import sys

# Relative import setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.macd_divergence.utils.helper import load_data, calculate_macd

# Page config
st.set_page_config(page_title="MACD Divergence Detector", layout="wide")
st.title("📉 MACD Divergence Detector")
st.subheader("Tracking MACD vs Signal line crossover zones (2020–2025)")

# Load and compute MACD
df = calculate_macd(load_data())

# Sidebar Date Filter
st.sidebar.header("🧭 Filter Options")
start_date = df["Date"].min().date()
end_date = df["Date"].max().date()

date_range = st.sidebar.slider(
    "Select Date Range",
    min_value=start_date,
    max_value=end_date,
    value=(start_date, end_date)
)

filtered_df = df[
    (df["Date"].dt.date >= date_range[0]) &
    (df["Date"].dt.date <= date_range[1])
]

# Chart
fig = go.Figure()

fig.add_trace(go.Scatter(x=filtered_df["Date"], y=filtered_df["MACD"], mode="lines", name="MACD", line=dict(color='blue')))
fig.add_trace(go.Scatter(x=filtered_df["Date"], y=filtered_df["Signal"], mode="lines", name="Signal", line=dict(color='orange')))

fig.update_layout(
    title="MACD & Signal Line Crossovers",
    xaxis_title="Date",
    yaxis_title="MACD Value",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

# Optional raw data
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df)
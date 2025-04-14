import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rsi_zones.utils.helper import load_data, calculate_rsi

# --- Page Config ---
st.set_page_config(page_title="RSI Reversal Zones Visualizer", layout="wide")
st.title("📉 RSI Reversal Zones Visualizer")
st.subheader("Detecting overbought/oversold levels in NASDAQ (2020–2025)")

# --- Load and Process Data ---
df = calculate_rsi(load_data())

# --- Sidebar Filter ---
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

# --- RSI Plot ---
fig = go.Figure()
fig.add_trace(go.Scatter(x=filtered_df["Date"], y=filtered_df["RSI"], mode="lines", name="RSI"))
fig.add_hline(y=70, line_dash="dash", line_color="red", name="Overbought")
fig.add_hline(y=30, line_dash="dash", line_color="green", name="Oversold")

fig.update_layout(
    title="RSI Indicator",
    xaxis_title="Date",
    yaxis_title="RSI Value",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

# --- Show Raw Data ---
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df)
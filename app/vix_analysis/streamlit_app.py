# app/vix_analysis/streamlit_app.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Set Streamlit page config
st.set_page_config(page_title="VIX Volatility Visualizer", layout="wide")

# Title and Description
st.title("📉 VIX Volatility Visualizer")
st.markdown("### Analyzing market fear index from **2020 to 2025**")

# Load VIX data
@st.cache_data
def load_vix_data():
    df = pd.read_csv("data/vix_2020_2025.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_vix_data()

# Sidebar controls
st.sidebar.header("🔍 Filter Options")
min_date = df["Date"].min()
max_date = df["Date"].max()

date_range = st.sidebar.slider(
    "Select Date Range",
    min_value=min_date.date(),
    max_value=max_date.date(),
    value=(min_date.date(), max_date.date())
)

# Filter data
df_filtered = df[(df["Date"].dt.date >= date_range[0]) & (df["Date"].dt.date <= date_range[1])]

# Interactive Plotly chart
st.subheader(f"📊 VIX Closing Price from {date_range[0]} to {date_range[1]}")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df_filtered["Date"],
    y=df_filtered["Close"],
    mode="lines+markers",
    line=dict(color="orange"),
    marker=dict(size=4),
    name="VIX Close"
))

fig.update_layout(
    title="VIX Index Over Time",
    xaxis_title="Date",
    yaxis_title="VIX Close",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white"),
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# Optional: Show table
if st.checkbox("Show Raw Data"):
    st.dataframe(df_filtered)
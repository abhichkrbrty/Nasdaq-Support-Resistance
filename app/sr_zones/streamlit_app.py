import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import sys
import os

# Setup for module import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.sr_detection import get_support_resistance

# Page config
st.set_page_config(page_title="NASDAQ Support & Resistance", layout="wide")
st.title("📈 NASDAQ Index Support & Resistance (2020–2025)")

# Load and clean data
@st.cache_data
def load_data():
    df = pd.read_csv("data/nasdaq_2020_2025.csv", parse_dates=['Date'], index_col='Date')
    for col in ['Open', 'High', 'Low', 'Close']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

data = load_data()

# Sidebar controls
st.sidebar.header("Controls")

# Time Range Selector
timeframe = st.sidebar.selectbox("Time Range", ["2 Weeks", "1 Month", "6 Months", "1 Year", "Max"])

# Zone Style & Quantity
zone_limit = st.sidebar.slider("Number of S/R Zones", min_value=5, max_value=50, value=20)
zone_style = st.sidebar.radio("Zone Style", ["Lines", "Bands"])

# Filter data by timeframe
def filter_data_by_timeframe(df, range_str):
    last_date = df.index[-1]
    if range_str == "2 Weeks":
        return df[df.index >= last_date - pd.Timedelta(weeks=2)]
    elif range_str == "1 Month":
        return df[df.index >= last_date - pd.DateOffset(months=1)]
    elif range_str == "6 Months":
        return df[df.index >= last_date - pd.DateOffset(months=6)]
    elif range_str == "1 Year":
        return df[df.index >= last_date - pd.DateOffset(years=1)]
    else:
        return df  # Max

filtered_data = filter_data_by_timeframe(data, timeframe)

# Get support/resistance zones for filtered data
zones = get_support_resistance(filtered_data)
zones = zones[:zone_limit]

# Plotting
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=filtered_data.index,
    y=filtered_data["Close"],
    mode="lines",
    name="NASDAQ Close",
    line=dict(color='deepskyblue')
))

# Add support/resistance zones
for z in zones:
    if zone_style == "Lines":
        fig.add_shape(
            type="line",
            x0=filtered_data.index[0], x1=filtered_data.index[-1],
            y0=z, y1=z,
            line=dict(color="red", dash="dash")
        )
    else:
        fig.add_shape(
            type="rect",
            x0=filtered_data.index[0], x1=filtered_data.index[-1],
            y0=z - 40, y1=z + 40,
            fillcolor="rgba(255,0,0,0.2)",
            line=dict(width=0)
        )

# Chart layout
fig.update_layout(
    title=f"NASDAQ Index with S/R Zones ({timeframe})",
    xaxis_title="Date",
    yaxis_title="Price",
    template="plotly_dark",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)
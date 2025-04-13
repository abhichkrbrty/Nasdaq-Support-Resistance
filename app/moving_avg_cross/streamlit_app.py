import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from app.moving_avg_cross.utils.helper import load_data, calculate_moving_averages, get_crossovers

# Page Config
st.set_page_config(page_title="Moving Average Crossover Detector", layout="wide")
st.title("📈 Moving Average Crossover Detector")
st.subheader("Visualizing Golden & Death Cross patterns (2020–2025)")

# Load & process data
df = load_data()
df = calculate_moving_averages(df)
df = get_crossovers(df)

# Filter Date Range
st.sidebar.header("🧭 Filter Options")
start_date = df["Date"].min().date()
end_date = df["Date"].max().date()

date_range = st.sidebar.slider("Select Date Range",
                               min_value=start_date,
                               max_value=end_date,
                               value=(start_date, end_date),
                               format="YYYY-MM-DD")

# Convert back to datetime for filtering
filtered_df = df[(df["Date"].dt.date >= date_range[0]) & (df["Date"].dt.date <= date_range[1])]

# Plot
fig = go.Figure()
fig.add_trace(go.Scatter(x=filtered_df["Date"], y=filtered_df["Close"], mode="lines", name="Close", line=dict(color="white")))
fig.add_trace(go.Scatter(x=filtered_df["Date"], y=filtered_df["MA50"], mode="lines", name="MA50", line=dict(color="blue")))
fig.add_trace(go.Scatter(x=filtered_df["Date"], y=filtered_df["MA200"], mode="lines", name="MA200", line=dict(color="orange")))

# Highlight Crossovers
crosses = filtered_df[filtered_df["Crossover"] != 0]
for _, row in crosses.iterrows():
    fig.add_shape(
        dict(
            type="line",
            x0=row["Date"], x1=row["Date"],
            y0=min(filtered_df["Close"]), y1=max(filtered_df["Close"]),
            line=dict(dash="dot", color="red" if row["Crossover"] == 2 else "green")
        )
    )

fig.update_layout(
    title="Moving Average Crossovers",
    xaxis_title="Date",
    yaxis_title="Price",
    template="plotly_dark",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# Option to show raw data
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df)
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from utils.sr_detection import get_support_resistance

st.set_page_config(page_title="NASDAQ Support & Resistance", layout="wide")

st.title("📈 NASDAQ Index Support & Resistance (2020–2025)")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("data/nasdaq_2020_2025.csv", parse_dates=['Date'], index_col='Date')

data = load_data()
fig = go.Figure()
fig.add_trace(go.Scatter(x=data.index, y=data["Close"], mode="lines", name="Close"))

# Support/Resistance Zones
zones = get_support_resistance(data)

for z in zones:
    fig.add_shape(
        type="line",
        x0=data.index[0],
        x1=data.index[-1],
        y0=z,
        y1=z,
        line=dict(color="red", dash="dash"),
    )

fig.update_layout(title="NASDAQ Index with S/R Zones", xaxis_title="Date", yaxis_title="Price")
st.plotly_chart(fig, use_container_width=True)
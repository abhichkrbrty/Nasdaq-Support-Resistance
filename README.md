# 📈 NASDAQ Support & Resistance Visualizer (2020–2025)

This project is a **Streamlit dashboard suite** that visualizes historical market behavior, fear indexes, and trading signals from 2020 to 2025 for the NASDAQ index. It includes:

### 🧭 Modules

| Chart | Description |
|-------|-------------|
| **VIX Volatility Visualizer** | Visualize the VIX (Fear Index) from 2020 to 2025 |
| **Support & Resistance Zones** | Detect and display dynamic S/R levels over custom intervals |
| **Moving Average Crossover** | Detect Golden Cross / Death Cross patterns |
| **RSI Reversal Zones** | Spot overbought / oversold RSI levels |
| **MACD Divergence Detector** | Visualize MACD and Signal line momentum shifts |

---

## 🚀 How to Run

```bash
git clone https://github.com/<your-username>/nasdaq-support-resistance.git
cd nasdaq-support-resistance
pip install -r requirements.txt
streamlit run app/vix_analysis/streamlit_app.py
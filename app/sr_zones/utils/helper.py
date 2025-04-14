import yfinance as yf
import pandas as pd

# Download
nasdaq = yf.download("^IXIC", start="2020-01-01", end="2025-04-10", interval="1d")

# Reset index so Date becomes a column
nasdaq.reset_index(inplace=True)

# Save clean version
nasdaq.to_csv("data/nasdaq_2020_2025.csv", index=False)
print("✅ Clean NASDAQ data saved")
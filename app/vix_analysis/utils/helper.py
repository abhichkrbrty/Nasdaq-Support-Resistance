# app/vix_analysis/helper.py

import yfinance as yf
import pandas as pd

def download_vix_data(path="data/vix_2020_2025.csv"):
    vix = yf.download('^VIX', start='2020-01-01', end='2025-01-01')
    vix.reset_index(inplace=True)
    vix.to_csv(path, index=False)
    print(f"✅ VIX data saved to {path}")

# 👇 Add this so it runs when you call the script directly
if __name__ == "__main__":
    download_vix_data()
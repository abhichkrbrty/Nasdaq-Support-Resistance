import pandas as pd

def load_data(path="data/nasdaq_2020_2025.csv"):
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")  # <- Force numeric type
    return df

def calculate_rsi(df, period=14):
    delta = df["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))
    return df
import pandas as pd

def load_data(path="data/nasdaq_2020_2025.csv"):
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
    df.dropna(subset=["Close"], inplace=True)
    return df

def calculate_moving_averages(df):
    df["MA50"] = df["Close"].rolling(window=50).mean()
    df["MA200"] = df["Close"].rolling(window=200).mean()
    return df

def get_crossovers(df):
    df["Signal"] = 0
    df.loc[df["MA50"] > df["MA200"], "Signal"] = 1
    df.loc[df["MA50"] < df["MA200"], "Signal"] = -1
    df["Crossover"] = df["Signal"].diff()
    return df
import pandas as pd
import numpy as np

def is_support(df, i):
    return df['Low'][i] < df['Low'][i - 1] and df['Low'][i] < df['Low'][i + 1] \
           and df['Low'][i + 1] < df['Low'][i + 2] and df['Low'][i - 1] < df['Low'][i - 2]

def is_resistance(df, i):
    return df['High'][i] > df['High'][i - 1] and df['High'][i] > df['High'][i + 1] \
           and df['High'][i + 1] > df['High'][i + 2] and df['High'][i - 1] > df['High'][i - 2]

def get_support_resistance(df):
    s_levels = []
    r_levels = []

    for i in range(2, df.shape[0] - 2):
        if is_support(df, i):
            level = df['Low'][i]
            if not s_levels or min([abs(level - sl) for sl in s_levels]) > 0.01 * level:
                s_levels.append(level)
        if is_resistance(df, i):
            level = df['High'][i]
            if not r_levels or min([abs(level - rl) for rl in r_levels]) > 0.01 * level:
                r_levels.append(level)

    return sorted(s_levels + r_levels)
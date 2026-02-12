import pandas as pd
from src.module.reports import track_changes
import numpy as np

@track_changes
def impute_amounts(df: pd.DataFrame) -> pd.DataFrame:
    if df is None:
        raise ValueError("DataFrame cannot de None")

    cols = ["Quantity", "Price Per Unit", "Total Spent"]

    for col in cols:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in DataFrame")

    df[cols] = df[cols].replace(["ERROR", "UNKNOWN"], np.nan)

    for col in cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        
    df["Total Spent"] = df["Total Spent"].fillna(df["Quantity"] * df["Price Per Unit"])
    df["Quantity"] = df["Quantity"].fillna(df["Total Spent"] / df["Price Per Unit"]).replace(0, np.nan)
    df["Price Per Unit"] =  df["Price Per Unit"].fillna(df["Total Spent"] / df["Quantity"]).replace(0, np.nan)

    return df
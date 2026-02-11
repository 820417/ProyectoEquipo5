import pandas as pd
from modulo.reportes import track_changes
import numpy as np

@track_changes
def rellenar_importes(df: pd.DataFrame) -> pd.DataFrame:
    if df is None:
        return None

    columnas = ["Quantity", "Price Per Unit", "Total Spent"]

    df[columnas] = df[columnas].replace("ERROR", np.nan)
    df[columnas] = df[columnas].replace("UNKNOWN", np.nan)

    df["Total Spent"] = df["Total Spent"].fillna(df["Quantity"] * df["Price Per Unit"])
    df["Quantity"] = df["Quantity"].fillna(df["Total Spent"] / df["Price Per Unit"]).replace(0, np.nan)
    df["Price Per Unit"] =  df["Price Per Unit"].fillna(df["Total Spent"] / df["Quantity"]).replace(0, np.nan)

    return df
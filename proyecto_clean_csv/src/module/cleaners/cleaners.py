from typing import Any, Literal

import pandas as pd
import numpy as np
from src.module.reports import track_changes


@track_changes
def remove_duplicate_rows(
    df: pd.DataFrame,
    columns: list[str] | None = None,
    keep: Literal["first", "last", False] = "first"
) -> pd.DataFrame:
    """Elimina filas duplicadas basándose en un subconjunto de columnas.

    Args:
        df: El DataFrame.
        columns: Lista de columnas que actúan como clave única para identificar duplicados.
                     Si es None, considera duplicada solo si TODA la fila es idéntica.
        keep: Qué duplicado mantener.
              'first' (la primera aparición), 'last' (la última), False (elimina todas).
    """
    return df.drop_duplicates(subset=columns, keep=keep).reset_index(drop=True)


@track_changes
def fill_null_values(
    df: pd.DataFrame,
    columns: list[str] | None = None,
    fill_value: Any = "UNKNOWN"
) -> pd.DataFrame:
    """Rellena los valores nulos con el valor especificado.

    Args:
        df: El DataFrame.
        columns: Lista de columnas donde aplicar el relleno. Si es None, aplica a todo el DF.
        fill_value: El valor que se insertará en los huecos.
    """
    df_clean = df.copy()

    if columns:
        df_clean[columns] = df_clean[columns].fillna(fill_value)
    else:
        df_clean = df_clean.fillna(fill_value)

    return df_clean

@track_changes
def impute_amounts(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Rellena los valores faltantes en las columnas "Quantity", "Price Per Unit" y "Total Spent"
    utilizando las relaciones matemáticas entre ellas.
    Si un valor no se puede calcular, se deja como NaN.

    :param df: El DataFrame a procesar.
    :rtype: pd.DataFrame
    :return: El DataFrame con los valores imputados.
    :rtype: pd.DataFrame
    """
    if df is None:
        raise ValueError("DataFrame cannot be None")

    cols = ["Quantity", "Price Per Unit", "Total Spent"]

    for col in cols:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in DataFrame")

    df["Total Spent"] = (
        df["Total Spent"]
        .fillna(df["Quantity"] * df["Price Per Unit"])
    )
    df["Quantity"] = (
        df["Quantity"]
        .fillna(df["Total Spent"] / df["Price Per Unit"])
        .replace(0, np.nan)
    )
    df["Price Per Unit"] = (
        df["Price Per Unit"]
        .fillna(df["Total Spent"] / df["Quantity"])
        .replace(0, np.nan)
    )

    return df

@track_changes
def drop_null_rows(
    df: pd.DataFrame,
    columns: list[str] | None = None
) -> pd.DataFrame:
    """Elimina las filas que contienen valores nulos.

    Args:
        df: El DataFrame.
        columns: Si se proporciona, solo busca nulos en estas columnas.
                        Si es None, revisa todas las columnas de la fila.
    """
    return df.dropna(subset=columns).reset_index(drop=True)


@track_changes
def convert_types_to_numeric(
    df: pd.DataFrame,
    columns: list[str] | None = None
) -> pd.DataFrame:
    """Intenta convertir las columnas especificadas a valores numéricos.

    Los valores que no se puedan convertir (ej: texto corrupto) se transformarán en NaN.

    Args:
        df: El DataFrame a procesar.
        columns: Lista de columnas a convertir.
    """
    df_clean = df.copy()
    cols_to_convert = columns if columns else df_clean.columns

    for col in cols_to_convert:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")

    return df_clean

from typing import Any, Literal

import numpy as np
import pandas as pd

from module.reports import track_changes, track_dtype_changes


@track_changes
def remove_duplicate_rows(
    df: pd.DataFrame,
    columns: list[str] | None = None,
    keep: Literal["first", "last", False] = "first",
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
    df: pd.DataFrame, columns: list[str] | None = None, fill_value: Any = "UNKNOWN"
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
def impute_amounts(df: pd.DataFrame) -> pd.DataFrame:
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

    df_clean = df.copy()
    cols = ["Quantity", "Price Per Unit", "Total Spent"]

    for col in cols:
        if col not in df_clean.columns:
            raise ValueError(f"Column '{col}' not found in DataFrame")

    df_clean["Total Spent"] = df_clean["Total Spent"].fillna(
        df_clean["Quantity"] * df_clean["Price Per Unit"]
    )
    df_clean["Quantity"] = (
        df_clean["Quantity"]
        .fillna(df_clean["Total Spent"] / df_clean["Price Per Unit"])
        .replace(0, np.nan)
    )
    df_clean["Price Per Unit"] = (
        df_clean["Price Per Unit"]
        .fillna(df_clean["Total Spent"] / df_clean["Quantity"])
        .replace(0, np.nan)
    )

    return df_clean


@track_changes
def drop_null_rows(df: pd.DataFrame, columns: list[str] | None = None) -> pd.DataFrame:
    """Elimina las filas que contienen valores nulos.

    Args:
        df: El DataFrame.
        columns: Si se proporciona, solo busca nulos en estas columnas.
                        Si es None, revisa todas las columnas de la fila.
    """
    return df.replace("UNKNOWN", np.nan).dropna(subset=columns).reset_index(drop=True)


@track_dtype_changes
def apply_schema_types(
    df: pd.DataFrame, column_types: dict[str, Any], error_report: dict[str, list[str]]
) -> pd.DataFrame:
    """Fuerza los tipos de datos basándose en el diccionario inyectado.

    Resuelve fechas y permite usar el tipo Int64.
    """
    df_clean = df.copy()

    cols_with_error = [col for col, errors in error_report.items() if "TYPE_ERROR" in errors]

    for col in cols_with_error:
        if col in column_types:
            dtype = column_types[col]

            if dtype in ["datetime", "datetime64[ns]"]:
                df_clean[col] = pd.to_datetime(df_clean[col], errors="coerce")
            elif dtype in ["int", "Int64"]:
                df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")
                df_clean[col] = df_clean[col].astype("Int64")
            elif dtype in ["float", "Float64"]:
                df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")
                df_clean[col] = df_clean[col].astype("Float64")
            else:
                try:
                    df_clean[col] = df_clean[col].astype(dtype)
                except (ValueError, TypeError):
                    pass

    return df_clean

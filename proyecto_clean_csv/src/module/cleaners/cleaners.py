from typing import Any, Literal

import pandas as pd
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

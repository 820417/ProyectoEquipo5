from typing import Any, Literal

import pandas as pd
from src.module.reports import track_changes


@track_changes
def remove_duplicate_rows(
    df: pd.DataFrame,
    key_columns: list[str] | None = None,
    keep: Literal["first", "last"] = "first"
) -> pd.DataFrame:
    """Elimina filas duplicadas basándose en un subconjunto de columnas.

    Args:
        df: El DataFrame.
        key_columns: Lista de columnas que actúan como clave única para identificar duplicados.
                     Si es None, considera duplicada solo si TODA la fila es idéntica.
        keep: Qué duplicado mantener.
              'first' (mantiene la primera aparición),
              'last' (mantiene la última),
              False (elimina todas las apariciones).
    """
    return df.drop_duplicates(subset=key_columns, keep=keep).reset_index(drop=True)


@track_changes
def fill_null_values(
    df: pd.DataFrame,
    value: Any,
    target_columns: list[str] | None = None
) -> pd.DataFrame:
    """Rellena los valores nulos con un valor específico (ej: 0, 'Desconocido', la media).

    Args:
        df: El DataFrame.
        value: El valor que se usará para rellenar los huecos.
        target_columns: Lista de columnas donde aplicar el relleno. Si es None, aplica a todo el DF.
    """
    df_clean = df.copy()

    if target_columns:
        df_clean[target_columns] = df_clean[target_columns].fillna(value)
    else:
        df_clean = df_clean.fillna(value)

    return df_clean


@track_changes
def drop_null_rows(
    df: pd.DataFrame,
    target_columns: list[str] | None = None
) -> pd.DataFrame:
    """Elimina las filas que contienen valores nulos (NaN/None).

    Args:
        df: El DataFrame.
        target_columns: Si se proporciona, solo busca nulos en estas columnas.
                        Si es None, revisa todas las columnas de la fila.
    """
    return df.dropna(subset=target_columns).reset_index(drop=True)

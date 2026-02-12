import pandas as pd
from src.module.reports import track_changes
from .protocol_cleaner import CleaningFunction


@track_changes
def remove_duplicate_rows(
    df: pd.DataFrame,
    columns: list[str] | None = None,
) -> pd.DataFrame:
    """Elimina filas duplicadas basándose en un subconjunto de columnas.

    Args:
        df: El DataFrame.
        columns: Lista de columnas que actúan como clave única para identificar duplicados.
                     Si es None, considera duplicada solo si TODA la fila es idéntica.
    """
    return df.drop_duplicates(subset=columns, keep="first").reset_index(drop=True)


@track_changes
def fill_null_values(
    df: pd.DataFrame,
    columns: list[str] | None = None
) -> pd.DataFrame:
    """Rellena los valores nulos con "UNKNOWN".

    Args:
        df: El DataFrame.
        columns: Lista de columnas donde aplicar el relleno. Si es None, aplica a todo el DF.
    """
    df_clean = df.copy()

    if columns:
        df_clean[columns] = df_clean[columns].fillna("UNKNOWN")
    else:
        df_clean = df_clean.fillna("UNKNOWN")

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

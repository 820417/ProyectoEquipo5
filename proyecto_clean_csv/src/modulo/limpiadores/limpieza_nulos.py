import pandas as pd


def limpiar_nulos(df: pd.DataFrame) -> pd.DataFrame:
    if df is None:
        return None

    df_limpio = df.fillna("UNKNOWN")

    filas_con_error = df_limpio.isin(['ERROR']).any(axis=1)
    indices_a_borrar = df_limpio[filas_con_error].index
    df_limpio = df_limpio.drop(indices_a_borrar)

    return df_limpio

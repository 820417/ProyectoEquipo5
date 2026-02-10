
def limpiar_nulos(df):
    if df is None:
        return None

    df_limpio = df.dropna()

    return df_limpio

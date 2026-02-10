import pandas as pd


def track_changes(func):

    def wrapper(*args, **kwargs):
        df_antes = next((arg for arg in args if isinstance(arg, pd.DataFrame)), None)
        filas_antes = len(df_antes) if df_antes is not None else 0

        resultado = func(*args, **kwargs)

        if isinstance(resultado, pd.DataFrame):
            filas_despues = len(resultado)
            diff = filas_antes - filas_despues
            if diff > 0:
                print(f"[LOG] {func.__name__}: Se han eliminado {diff} filas.")
            elif diff == 0:
                print(f"[LOG] {func.__name__}: Sin cambios en el número de filas.")

        return resultado
    return wrapper

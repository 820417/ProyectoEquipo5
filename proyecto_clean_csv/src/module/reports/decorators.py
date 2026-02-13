import pandas as pd
import logging

logger=logging.getLogger(__name__)

def track_changes(func):

    def wrapper(*args, **kwargs):
        df_antes = next((arg for arg in args if isinstance(arg, pd.DataFrame)), None)
        filas_antes = len(df_antes) if df_antes is not None else 0

        resultado = func(*args, **kwargs)

        if isinstance(resultado, pd.DataFrame):
            filas_despues = len(resultado)
            diff = filas_antes - filas_despues
            if diff > 0:
                logger.info(
                    "%s: Se han eliminado %d filas.",
                    func.__name__,
                    diff
                )
            elif diff == 0:
                logger.info(
                    "%s: Sin cambios en el número de filas.",
                    func.__name__
                )

        return resultado
    return wrapper

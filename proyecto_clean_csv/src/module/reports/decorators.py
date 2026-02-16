import logging
import time
from collections.abc import Callable
from typing import Any, Optional

import pandas as pd

logger = logging.getLogger(__name__)


def track_changes(_func: Callable | None = None, *, action: str | None = None):

    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            start = time.perf_counter()

            df_antes = next((arg for arg in args if isinstance(arg, pd.DataFrame)), None)
            filas_antes = len(df_antes) if df_antes is not None else 0

            if action:
                logger.info(
                    "Se inicia la ejecución de la función '%s'. Acción: %s.", func.__name__, action
                )
            else:
                logger.info("Se inicia la ejecución de la función '%s'.", func.__name__)
            result = func(*args, **kwargs)

            duration = time.perf_counter() - start

            if isinstance(result, pd.DataFrame) and filas_antes is not None:
                filas_despues = len(result)
                diff = filas_antes - filas_despues
                if diff > 0:
                    logger.info(
                        "La función '%s' ha finalizado. "
                        "Se han eliminado %d filas (antes: %d, después: %d).",
                        func.__name__,
                        diff,
                        filas_antes,
                        filas_despues,
                    )
                elif diff == 0:
                    logger.info(
                        "La función '%s' ha finalizado "
                        "sin cambios en el número de filas (total: %d).",
                        func.__name__,
                        filas_despues,
                    )
            logger.info("Tiempo de ejecución de '%s': %.4f segundos.", func.__name__, duration)

            return result

        return wrapper

    if _func is None:
        return decorator
    return decorator(_func)


def track_dtype_changes(func: Callable) -> Callable:

    def wrapper(*args, **kwargs):
        df_antes = next((arg for arg in args if isinstance(arg, pd.DataFrame)), None)

        tipos_antes = df_antes.dtypes.to_dict()

        result = func(*args, **kwargs)

        tipos_despues = result.dtypes.to_dict()

        logger.info("Resumen de cambios de tipos en la función '%s':", func.__name__)
        for col in tipos_despues:
            tipo_antes = tipos_antes.get(col, "No existía")
            tipo_despues = tipos_despues[col]

            logger.info(
                "Columna '%s' → Tipo antes: %s → Tipo después: %s", col, tipo_antes, tipo_despues
            )

        return result

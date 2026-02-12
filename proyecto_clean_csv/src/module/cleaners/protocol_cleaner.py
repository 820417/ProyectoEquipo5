from typing import Protocol

import pandas as pd


class CleaningFunction(Protocol):
    """Protocolo para funciones de limpieza de datos.

    Recibe un DataFrame y una lista opcional de columnas.
    Devuelve un DataFrame limpio.
    """
    def __call__(self, df: pd.DataFrame, columns: list[str] | None = None) -> pd.DataFrame:
        """Ejecuta la lógica de limpieza.

        Args:
            df: El DataFrame .
            columns: Lista de nombres de columnas específicas a las que aplicar la limpieza.
                     - Si es una lista: se limpian esas columnas.
                     - Si es None: La función aplica su comportamiento por defecto.

        Returns:
            pd.DataFrame: El DataFrame resultante después de la transformación.
                          Debe ser una copia o el mismo objeto modificado, pero nunca None.
        """
        ...

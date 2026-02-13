from typing import Any

import pandas as pd
from src.module.data_models.schema import (
    CRITICAL_COLUMNS,
    NUMERIC_COLUMNS,
    TRANSACTION_ID,
    DUPLICATED_VALUES_ERROR,
    NULL_VALUES_ERROR,
    TYPE_ERROR
)
from .cleaners import (
    convert_types_to_numeric,
    drop_null_rows,
    fill_null_values,
    remove_duplicate_rows,
    impute_amounts
)


class DataCleanerDispatcher:
    """Clase encargada de dirigir los errores detectados por el Validator."""
    def __init__(self, config: dict[str, Any]) -> None:
        """Recibe la configuración del cliente."""
        self.config = config

    def clean(self, df: pd.DataFrame, error_report: dict[str, list[str]]) -> pd.DataFrame:
        """Analiza el diccionario de errores y aplica las transformaciones necesarias.

        Args:
            df: El DataFrame sucio recibido del Validator.
            error_report: Diccionario con formato {"Columna": ["ERROR_1", "ERROR_2"]}

        Returns:
            pd.DataFrame: El DataFrame limpio.
        """
        df_clean = df.copy()

        null_strategy = self.config.get("null_strategy", "fill")
        fill_value = self.config.get("fill_value", "UNKNOWN")
        keep_duplicates = self.config.get("keep_duplicates", "first")

        # 1. Eliminar elementos duplicados de "Transaction ID"
        if (TRANSACTION_ID in error_report and
                DUPLICATED_VALUES_ERROR in error_report[TRANSACTION_ID]):
            df_clean = remove_duplicate_rows(
                df_clean,
                columns=[TRANSACTION_ID],
                keep=keep_duplicates
            )

        # 2. Conversión de columnas a numéricas antes de la imputación
        # TODO: Falta convertir la columna de fecha (y si se puede "Quantity" a int),
        #  -> los tipos están en schema.py en la const COLUMN_TYPES
        df_clean = convert_types_to_numeric(df_clean, NUMERIC_COLUMNS)

        # 3. Imputar valores faltantes en "Quantity", "Price Per Unit" y "Total Spent"
        df_clean = impute_amounts(df_clean)

        # 4. Manejo de valores nulos restantes según la estrategia definida
        critical_to_drop = [
            col for col in error_report
            if NULL_VALUES_ERROR in error_report[col] and col in CRITICAL_COLUMNS
        ]
        optional_to_fill = [
            col for col in error_report
            if NULL_VALUES_ERROR in error_report[col] and col not in CRITICAL_COLUMNS
        ]

        # 4.1 Drop nulos en columnas críticas
        if critical_to_drop:
            df_clean = drop_null_rows(df_clean, columns=critical_to_drop)

        # 4.2 Rellenar nulos en columnas opcionales
        if optional_to_fill:
            df_clean = fill_null_values(df_clean, columns=optional_to_fill, fill_value=fill_value)

        return df_clean

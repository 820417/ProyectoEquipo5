from typing import Any

import pandas as pd
from src.module.cleaners.cleaners import (
    convert_types_to_numeric,
    drop_null_rows,
    fill_null_values,
    remove_duplicate_rows,
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

        for column_name, errors in error_report.items():

            if "NULL_VALUES" in errors:
                if null_strategy == "drop":
                    df_clean = drop_null_rows(df_clean, columns=[column_name])
                else:
                    df_clean = fill_null_values(df_clean, columns=[column_name],
                                                fill_value=fill_value)

            if "DUPLICATES" in errors:
                df_clean = remove_duplicate_rows(
                    df_clean,
                    columns=[column_name],
                    keep=keep_duplicates
                )

            if "TYPE_ERROR" in errors:
                df_clean = convert_types_to_numeric(
                    df_clean,
                    columns=[column_name]
                )

        return df_clean

from typing import Any

import pandas as pd

from module.data_models.schema import (
    COLUMN_TYPES,
    CRITICAL_COLUMNS,
    DUPLICATED_VALUES_ERROR,
    ITEM_TO_CATEGORY,
    NULL_VALUES_ERROR,
    TRANSACTION_ID,
)

from .cleaners import (
    apply_schema_types,
    drop_null_rows,
    fill_null_values,
    impute_amounts,
    impute_category_from_item,
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

        dup_config = self.config.get("duplicates", {})
        types_config = self.config.get("types", {})
        impute_config = self.config.get("imputation", {})
        nulls_config = self.config.get("nulls", {})
        # null_strategy = self.config.get("null_strategy", "fill")
        # fill_value = self.config.get("fill_value", "UNKNOWN")
        # keep_duplicates = self.config.get("keep_duplicates", "first")

        # 1. Eliminar elementos duplicados de "Transaction ID"
        if dup_config.get("apply", False):
            if (
                TRANSACTION_ID in error_report
                and DUPLICATED_VALUES_ERROR in error_report[TRANSACTION_ID]
            ):
                df_clean = remove_duplicate_rows(
                    df_clean, columns=[TRANSACTION_ID], keep=dup_config.get("keep", "first")
                )

        # 2. Conversión de columnas a numéricas antes de la imputación
        # TODO: Falta convertir la columna de fecha (y si se puede "Quantity" a int),
        #  -> los tipos están en schema.py en la const COLUMN_TYPES
        if types_config.get("apply", False):
            df_clean = apply_schema_types(df_clean, COLUMN_TYPES)

        print(df_clean.info())

        # 3. Imputar valores faltantes en "Quantity", "Price Per Unit" y "Total Spent"
        if impute_config.get("apply_amounts", False):
            df_clean = impute_amounts(df_clean)

        # 3.2 Imputar categorías basándose en el Item
        if impute_config.get("apply_category", False):
            df_clean = impute_category_from_item(df_clean, ITEM_TO_CATEGORY)

        # 4. Manejo de valores nulos restantes según la estrategia definida
        critical_to_drop = [
            col
            for col in error_report
            if NULL_VALUES_ERROR in error_report[col] and col in CRITICAL_COLUMNS
        ]

        # 4.1 Drop nulos en columnas críticas
        if critical_to_drop:
            df_clean = drop_null_rows(df_clean, columns=critical_to_drop)

        # 4.2 Fill nulos opcionales autorizados por el JSON
        if nulls_config.get("apply", False):
            allowed_cols = nulls_config.get("columns", [])
            cols_to_fill = [
                col
                for col in error_report
                if NULL_VALUES_ERROR in error_report.get(col, [])
                and col in allowed_cols
                and col not in CRITICAL_COLUMNS
            ]
            if cols_to_fill:
                df_clean = fill_null_values(
                    df_clean,
                    columns=cols_to_fill,
                    fill_value=nulls_config.get("fill_value", "UNKNOWN"),
                )

        return df_clean

from typing import Any

import pandas as pd

from module.data_models.schema import (
    COLUMN_TYPES,
    DUPLICATED_VALUES_ERROR,
    NULL_VALUES_ERROR,
    TRANSACTION_ID,
    TYPE_ERROR,
)

from .base_validator import Validator


class NullValidator(Validator):
    """
    Validador para detectar valores nulos en el DataFrame.
    """
    def validate(self, df: pd.DataFrame, config: dict[str, Any]) -> dict[str, list[str]]:
        """
        Recorre cada columna del DataFrame y si encuentra valores nulos agrega un error
        al diccionario de errores con el nombre de la columna y el mensaje "NULL_VALUES".

        :param df: DataFrame de pandas a validar.
        :type df: pd.DataFrame
        :return: Diccionario con los errores encontrados.
        :rtype: dict[str, list[str]]
        """
        if not config.get("validations", {}).get("validate_nulls", False):
            return {}

        errors = {}
        for col in df.columns:
            if df[col].isnull().any():
                errors.setdefault(col, []).append(NULL_VALUES_ERROR)

        return errors

class DuplicateValidator(Validator):

    def __init__(self, key_column: str = TRANSACTION_ID) -> None:
        self._key_column = key_column

    def validate(self, df: pd.DataFrame, config: dict[str, Any]) -> dict[str, list[str]]:
        """
        Comprueba si la columna "Transaction ID" del DataFrame contiene valores duplicados.
        Si encuentra, agrega un error al diccionario de errores con el nombre de la columna y
        el mensaje "DUPLICATED_VALUES".

        :param df: DataFrame de pandas a validar.
        :type df: pd.DataFrame
        :return: Diccionario con los errores encontrados.
        :rtype: dict[str, list[str]]
        """
        if not config.get("validations", {}).get("validate_duplicates", False):
            return {}

        errors = {}

        if df[self._key_column].duplicated().any():
            errors.setdefault(self._key_column, []).append(DUPLICATED_VALUES_ERROR)

        return errors

class TypeValidator(Validator):

    def __init__(self) -> None:
        """
        Inicializa validador de tipos con un diccionario que mapea cada columna a su tipo esperado.
        """
        self._types = COLUMN_TYPES

    def validate(self, df: pd.DataFrame, config: dict[str, Any]) -> dict[str, list[str]]:
        """
        Recorre cada columna del DataFrame y verifica si los valores pueden ser convertidos al tipo
        esperado. Si encuentra valores que no pueden ser convertidos, agrega un error al diccionario
        de errores con el nombre de la columna y el mensaje "TYPE_ERROR".

        :param df: DataFrame de pandas a validar.
        :type df: pd.DataFrame
        :return: Diccionario con los errores encontrados.
        :rtype: dict[str, list[str]]
        """

        if not config.get("validations", {}).get("validate_types", False):
            return {}

        errors = {}

        for col, expected_type in self._types.items():

            if col not in df.columns:
                continue

            if expected_type in ["int", "float"]:
                converted = pd.to_numeric(df[col], errors="coerce")
                if converted.isna().sum() > df[col].isna().sum():
                    errors.setdefault(col, []).append(TYPE_ERROR)

            elif expected_type == "datetime":
                converted = pd.to_datetime(df[col], errors="coerce")
                if converted.isna().sum() > df[col].isna().sum():
                    errors.setdefault(col, []).append(TYPE_ERROR)

        return errors

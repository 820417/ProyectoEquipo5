from .base_validator import Validator
import pandas as pd
from typing import Any, Dict


class NullValidator(Validator):
    """
    Validador para detectar valores nulos en el DataFrame.
    """
    def validate(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Recorre cada columna del DataFrame y si encuentra valores nulos agrega un error
        al diccionario de errores con el nombre de la columna y el mensaje "NULL_VALUES".

        :param df: DataFrame de pandas a validar.
        :type df: pd.DataFrame 
        :return: Diccionario con los errores encontrados.
        :rtype: Dict[str, Any]
        """
        errors = {}
        for col in df.columns:
            if df[col].isnull().any():
                errors[col] = "NULL_VALUES"

        return errors
    
class DuplicateValidator(Validator):

    def __init__(self, key_column: str = "Transaction ID") -> None:
        self.key_column = key_column

    def validate(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Comprueba si la columna "Transaction ID" del DataFrame contiene valores duplicados.
        Si encuentra, agrega un error al diccionario de errores con el nombre de la columna y el mensaje "DUPLICATED_VALUES".

        :param df: DataFrame de pandas a validar.
        :type df: pd.DataFrame
        :return: Diccionario con los errores encontrados.
        :rtype: Dict[str, Any]
        """
        
        errors = {}

        if df[self.key_column].duplicated().any():
            errors[self.key_column] = "DUPLICATED_VALUES"

        return errors
    
class TypeValidator(Validator):

    def __init__(self):
        """
        Inicializa el validador de tipos con un diccionario que mapea cada columna a su tipo esperado.
        """
        self.types = {
            "Transaction ID": "str",
            "Item": "str",
            "Quantity": "int",
            "Price Per Unit": "float",
            "Total Spent": "float",
            "Payment Method": "str",
            "Location": "str",
            "Transaction Date": "datetime64[ns]"
        }

    def validate(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Recorre cada columna del DataFrame y verifica si el tipo de datos coincide con el tipo esperado.
        Si el tipo no coincide, agrega un error al diccionario de errores con el nombre de la columna y el mensaje "TYPE_ERROR".

        :param df: DataFrame de pandas a validar.
        :type df: pd.DataFrame
        :return: Diccionario con los errores encontrados.
        :rtype: Dict[str, Any]
        """
        errors = {}

        for col in df.columns:
            if not isinstance(type(col), self.types[col]):
                errors[col] = "TYPE_ERROR"
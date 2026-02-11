from .base_validator import Validator
import pandas as pd
from typing import Any, Dict


class NullValidator(Validator):

    def validate(self, df: pd.DataFrame) -> Dict[str, Any]:
        errors = {}
        for col in df.columns:
            if df[col].isnull().any():
                errors[col] = "NULL_VALUES"

        return errors
    
class DuplicateValidator(Validator):

    def validate(self, df: pd.DataFrame) -> Dict[str, Any]:
        errors = {}

        if df["Transaction ID"].duplicated().any():
            errors["Transaction ID"] = "DUPLICATED_VALUES"

        return errors
    
class TypeValidator(Validator):

    def __init__(self):
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
        errors = {}

        for col in df.columns:
            if not isinstance(type(col), self.tipos[col]):
                errors[col] = "TYPE_ERROR"
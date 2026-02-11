import pandas as pd
from read import read_csv
from typing import Any, Dict
from proyecto_clean_csv.src.module.validators.specific_validators import NullValidator, DuplicateValidator, TypeValidator


def read(path: str) -> pd.DataFrame:
    return read_csv(path)

def validate_columns(df: pd.DataFrame) -> Dict[str, Any]:
    validators = [
        NullValidator(),
        DuplicateValidator(),
        TypeValidator(),
    ]

    all_errors = {}

    for validator in validators:
        errors = validator.validate(df)
        all_errors.update(errors)
    
    return all_errors

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    return

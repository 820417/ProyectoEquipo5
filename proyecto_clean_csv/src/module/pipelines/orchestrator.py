import pandas as pd
from typing import Any, Dict
from src.module.cleaners.remove_duplicates import limpiador_duplicados_por_id
from src.module.cleaners.remove_nulls import limpiar_nulos
from src.module.data_models.transform.fill_data import impute_amounts
from src.module.read import get_csv_reader
from src.module.validators import Validator, NullValidator, DuplicateValidator, TypeValidator
from collections import defaultdict


class DataPipelineOrchestrator:
    def __init__(self, path: str):
        self.path = path
    
    def run(self):
        df = self._read_file()
        print(df.info())
        df = self._process(df)
        self._report(df)
        print(df.head())
    

    def _read_file(self) -> pd.DataFrame:
        reader = get_csv_reader(self.path)
        return reader.read(self.path)
    
    def _process(self, df: pd.DataFrame) -> pd.DataFrame:
        diccionario = self._validacion(df)
        print(diccionario)
        df = self._transformacion(df)
        df = self._limpieza(df)
        return df

    def _report(self, df: pd.DataFrame) -> pd.DataFrame:
        return df


    def _validacion(self, df: pd.DataFrame) -> Dict[str, Any]:
        validators: list[Validator]= [
            NullValidator(),
            DuplicateValidator(),
            TypeValidator(),
        ]

        all_errors: dict[str, list] = defaultdict(list)

        for validator in validators:
            errors = validator.validate(df)

            for column, error in errors.items():
                all_errors[column].append(error)

        return dict(all_errors)

    def _transformacion(self, df: pd.DataFrame) -> pd.DataFrame:
        df = impute_amounts(df)
        # df = add_quarter_column(df)
        return df
    
    def _limpieza(self, df: pd.DataFrame) -> pd.DataFrame:
        df = limpiador_duplicados_por_id(df)
        df = limpiar_nulos(df)
        return df
    
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

import pandas as pd
from src.module.cleaners.cleaner_dispatcher import DataCleanerDispatcher
from src.module.read import get_csv_reader
from src.module.validators import DuplicateValidator, NullValidator, TypeValidator, Validator


class DataPipelineOrchestrator:
    def __init__(self, path: str, config_path: str):
        self.path = path
        self.config = self._load_config(config_path)

    def _load_config(self, config_path: str) -> dict:
        """Lee el archivo config.json y lo convierte en un diccionario."""
        with Path(config_path).open() as file:
            return json.load(file)

    def run(self) -> None:
        df = self._read_file()
        df = self._process(df)
        self._report(df)
        print(df.info())

    def _read_file(self) -> pd.DataFrame:
        reader = get_csv_reader(self.path)
        return reader.read(self.path)

    def _process(self, df: pd.DataFrame) -> pd.DataFrame:
        diccionario = self._validacion(df)
        print(diccionario)
        df = self._limpieza(df, diccionario)
        return self._transformacion(df)

    def _report(self, df: pd.DataFrame) -> pd.DataFrame:
        return df


    def _validacion(self, df: pd.DataFrame) -> dict[str, Any]:
        validators: list[Validator]= [
            NullValidator(),
            DuplicateValidator(),
            TypeValidator(),
        ]

        all_errors: dict[str, list] = defaultdict(list)

        for validator in validators:
            errors = validator.validate(df)

            for column, error_list in errors.items():
                all_errors[column].extend(error_list)

        return dict(all_errors)

    def _transformacion(self, df: pd.DataFrame) -> pd.DataFrame:
        # df = add_quarter_column(df)
        return df

    def _limpieza(self, df: pd.DataFrame, error_report: dict[str, list]) -> pd.DataFrame:
        dispatcher = DataCleanerDispatcher(self.config)
        return dispatcher.clean(df, error_report)

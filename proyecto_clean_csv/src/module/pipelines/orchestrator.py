import json
import logging
from collections import defaultdict
from pathlib import Path

import pandas as pd

from module.cleaners.cleaner_dispatcher import DataCleanerDispatcher
from module.read import get_csv_reader
from module.reports import csv_exporter
from module.reports.plot_generator import BarPlot
from module.transforms import add_category_column, add_weekday_column, add_year_third_column
from module.validators import DuplicateValidator, NullValidator, TypeValidator, Validator

logger = logging.getLogger(__name__)

class DataPipelineOrchestrator:
    def __init__(self, path: str | Path, config_path: str | Path, base_dir: str | Path) -> None:
        """
        Orquestador del pipeline

        :param path: Ruta del archivo CSV a procesar.
        :param config_path: Ruta del archivo de configuración JSON.
        :param base_dir: Ruta base del proyecto para generar archivos de salida.
        """
        self.path = Path(path)
        self.name: str = self.path.stem
        self._base_dir = Path(base_dir)
        self.config = self._load_config(config_path)

    def _load_config(self, config_path: str | Path) -> dict:
        """Lee el archivo config.json y lo convierte en un diccionario."""
        config_path = Path(config_path)

        with Path(config_path).open() as file:
            return json.load(file)

    def run(self) -> None:
        df = self._read_file()
        df = self._process(df)
        self._report(df)

    def _read_file(self) -> pd.DataFrame:
        reader = get_csv_reader(self.path)
        return reader.read(self.path)

    def _process(self, df: pd.DataFrame) -> pd.DataFrame:
        errors_dict = self._validacion(df)
        df = self._limpieza(df, errors_dict)
        df = self._transformacion(df)
        return df

    def _report(self, df: pd.DataFrame) -> pd.DataFrame:
        csv_exporter(self, df)
        self._generate_plots(df)
        return df


    def _validacion(self, df: pd.DataFrame) -> dict[str, list[str]]:
        """
        Realiza la validación del DataFrame utilizando los validadores definidos.
        Si el DataFrame está vacío, devuelve un error indicando que no contiene filas.

        :param df: DataFrame de pandas a validar.
        :type df: pd.DataFrame
        :return: Diccionario con los errores encontrados de cada columna.
        :rtype: dict[str, list[str]]
        """
        if df.empty:
            return {"__dataframe__": ["El DataFrame no contiene filas"]}

        validators: list[Validator]= [
            NullValidator(),
            DuplicateValidator(),
            TypeValidator(),
        ]

        all_errors: dict[str, list] = defaultdict(list)

        for validator in validators:
            errors = validator.validate(df, self.config)

            for column, error_list in errors.items():
                all_errors[column].extend(error_list)

        if all_errors:
            logger.info(
                "Errores de validación encontrados:\n%s",
                json.dumps(all_errors, indent=2, ensure_ascii=False)
            )

        return dict(all_errors)

    def _transformacion(self, df: pd.DataFrame) -> pd.DataFrame:
        df = add_year_third_column(df)
        df = add_weekday_column(df)
        df = add_category_column(df)
        return df

    def _limpieza(self, df: pd.DataFrame, error_report: dict[str, list]) -> pd.DataFrame:
        dispatcher = DataCleanerDispatcher(self.config)
        return dispatcher.clean(df, error_report)

    def _generate_plots(self, df: pd.DataFrame):
        plots = [
            BarPlot(
                df,
                self._base_dir,
                f"{self.name}",
                column="Category",
                title="Categorías",
                xlabel="Categoría",
                ylabel="Cantidad"
            ),
            BarPlot(
                df, self._base_dir,
                f"{self.name}",
                column="Year third",
                title="Tercio del año",
                xlabel="Tercio del Año",
                ylabel="Cantidad"
            ),
            BarPlot(
                df,
                self._base_dir,
                f"{self.name}",
                column="Weekday",
                title="Día de la Semana",
                xlabel="Día de la Semana",
                ylabel="Cantidad"
            ),
        ]


        for plot in plots:
            plot.plot()


import csv
from typing import Protocol

import pandas as pd


class ReaderCSV(Protocol) :
    def read(self, path: str) -> pd.DataFrame:
        """
        Lee un archivo CSV y devuelve un DataFrame.

        :param path: Ruta del archivo CSV.
        :type path: str
        :return: DataFrame de pandas con los datos del CSV.
        :rtype: pd.DataFrame
        """
        ...


class ReaderCSVPandas(ReaderCSV):
    """
    Clase para leer archivos CSV usando pandas.
    """
    def read(self, path: str) -> pd.DataFrame:
        """
        Lee un archivo CSV y devuelve un DataFrame de pandas.

        :param path: Ruta del archivo CSV.
        :type path: str
        :return: DataFrame de pandas con los datos del CSV.
        :rtype: pd.DataFrame
        """
        try:
            df = pd.read_csv(path,
                            sep=None,
                            engine="python",
                            header=0)
            return df

        except FileNotFoundError as e:
            raise FileNotFoundError("Archivo CSV no econtrado.") from e
        except Exception as e:
            raise Exception("Error al leer el CSV") from e


class ReaderCSVGenerator(ReaderCSV):
    """
    Clase para leer archivos CSV usando un generador.
    """
    def read(self, path: str) -> pd.DataFrame:
        """
        Lee un archivo CSV usando un generador y devuelve un DataFrame.

        :param path: Ruta del archivo CSV.
        :type path: str
        :return: DataFrame de pandas con los datos del CSV.
        :rtype: pd.DataFrame
        """
<<<<<<< HEAD
        filas = self._read_generator(path)
        return pd.DataFrame(filas)
=======
        try:
            filas = self._read_generator(path)
            return pd.DataFrame(filas)

        except FileNotFoundError as e:
            raise FileNotFoundError("Archivo CSV no econtrado.") from e
        except Exception as e:
            raise Exception("Error al leer el CSV") from e
>>>>>>> 36392c80d75d4a26104a2663ff30862cafaad26e

    def _read_generator(self, path: str):
        """
        Generador que lee un archivo CSV y devuelve filas en forma de diccionarios.

        :param path: Ruta del archivo CSV.
        :type path: str
        :yield: Diccionarios con los datos de cada fila.
        :rtype: dict
        """
        with open(path, encoding='utf-8') as fichero:
            lector = csv.DictReader(fichero)
            yield from lector

import pandas as pd
from typing import Generator, Dict, Any, Protocol
import csv

#from contextlib import contextmanager

class ReaderCSV:
    def read(self, path: str, read_mode: str = "pandas") -> pd.DataFrame:
        """
        Docstring for read
        
        :param self: Description
        :param path: Description
        :type path: str
        :param read_mode: Description
        :type read_mode: str
        :return: Description
        :rtype: DataFrame
        """
        if read_mode == "pandas":
            reader = ReaderCSVPandas()
        elif read_mode == "generator":
            reader = ReaderCSVGenerator()
        else:
            raise ValueError("Tipo no válido")
        
        return reader.read(path)

class ReaderCSVPandas:
    """
    Docstring for ReaderCSVPandas
    """
    def read(self, path: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(path,
                            sep=None,
                            engine="python")
            return df

        except FileNotFoundError as e:
            raise FileNotFoundError("El archivo no existe.") from e
        except Exception as e:
            raise Exception("Error al leer el CSV") from e


class ReaderCSVGenerator:
    def read(self, path: str) -> pd.DataFrame:
        """
        Docstring for read
        
        :param self: Description
        :param path: Description
        :type path: str
        :return: Description
        :rtype: DataFrame
        """
        filas = self._read_generator(path)
        return pd.DataFrame(filas)
        
    def _read_generator(self, path: str):
        """
        Docstring for _read_generator
        
        :param self: Description
        :param path: Description
        :type path: str
        """
        with open(path, 'r', encoding='utf-8') as fichero:
            lector = csv.DictReader(fichero)
            for linea in lector:
                yield linea

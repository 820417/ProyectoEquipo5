import os

from .reader import ReaderCSV, ReaderCSVGenerator, ReaderCSVPandas

SIZE_THRESHOLD = 2 * 1024 * 1024  # 2MB

def get_csv_reader(path: str) -> ReaderCSV:
    """
    Detecta la forma en la que se debe leer el fichero CSV según su tamaño.
    Seleciona Pandas o generador.

    :param path: Ruta del archivo CSV.
    :type path: str
    :return: Clase del lector seleccionada
    :rtype: ReaderCSV
    """
    size = os.path.getsize(path)

    if size < SIZE_THRESHOLD:
        return ReaderCSVPandas()
    else:
        return ReaderCSVGenerator()

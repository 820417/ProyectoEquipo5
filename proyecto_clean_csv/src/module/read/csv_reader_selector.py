import os
from .reader import ReaderCSVPandas, ReaderCSVGenerator, ReaderCSV


SIZE_THRESHOLD = 2 * 1024 * 1024

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
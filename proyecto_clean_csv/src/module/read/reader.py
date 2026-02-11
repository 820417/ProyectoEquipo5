import pandas as pd
from typing import Generator, Dict, Any
#from contextlib import contextmanager

path = "../../../examples/retail_store_sales.csv"
def read_csv(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path,
                         sep=None,
                         engine="python")
        return df

    except FileNotFoundError as e:
        raise FileNotFoundError("El archivo no existe.") from e
    except Exception as e:
        raise Exception("Error al leer el CSV") from e


#@contextmanager
#def abrir_archivo(path: str):
#        f = open(path, "r", encoding="utf-8", errors="replace")
#       try:
#                yield f
#        finally:
#                f.close() 

#def generador_csv(path: str) -> Generator[Dict[str,Any], None, None]:
#        with abrir_archivo(path) as f:
#                read_csv=csv.Dictread_csv(f)

#                for fila in read_csv:
#                        yield fila
import pandas as pd
from typing import Generator, Dict, Any
#from contextlib import contextmanager

path = "../../../examples/retai_store_sales.csv"
def reader(path: str) -> pd.DataFrame:
#    try:
        df = pd.read_csv(path,
                         sep=None,
                         engine="python")
        return df

#    except FileNotFoundError:
#        print("El archivo no existe.")
#        return None

#    except Exception as e:
#        print(f"Erro al leer el CSV:{e}")
#        return None


#@contextmanager
#def abrir_archivo(path: str):
#        f = open(path, "r", encoding="utf-8", errors="replace")
#       try:
#                yield f
#        finally:
#                f.close() 

#def generador_csv(path: str) -> Generator[Dict[str,Any], None, None]:
#        with abrir_archivo(path) as f:
#                reader=csv.DictReader(f)

#                for fila in reader:
#                        yield fila
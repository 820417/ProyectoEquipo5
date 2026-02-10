import pandas as pd
from typing import Generator, Dict, Any

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

# def generador_csv(path: str) -> Generator[Dict[str,Any], None, None]:

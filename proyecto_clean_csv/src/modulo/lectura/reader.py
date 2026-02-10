import pandas as pd

path = "../../../examples/retai_store_sales.csv"
def reader(path):
    try:
        df = pd.read_csv(path,
                         sep=None,
                         engine="python")
        return df
    except FileNotFoundError:
        print("El archivo no existe.")
        return None
    
    except Exception as e:
        print(f"Erro al leer el CSV:{e}")
        return None

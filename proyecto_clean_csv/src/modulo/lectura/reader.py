import pandas as pd

path = "../../../examples/retai_store_sales.csv"
def reader(path):
    try:
        df = pd.read_csv(path)
        return df
    except FileNotFoundError:
        print("El archivo no existe.")
        return None

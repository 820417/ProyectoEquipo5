from src.module.cleaners.remove_duplicates import limpiador_duplicados_por_id
from src.module.cleaners.remove_nulls import limpiar_nulos
from src.module.data_models.transform.fill_data import impute_amounts
from src.module.read.reader import ReaderCSV


def main():
    reader = ReaderCSV()
    df = reader.read("proyecto_clean_csv/examples/ventas_cafe.csv", "generator")

    df_filled = impute_amounts(df)

    df_no_duplicates = limpiador_duplicados_por_id(df_filled)

    df_clean = limpiar_nulos(df_no_duplicates)

    print("***********************************")
    print(df_clean.head())
    print("***********************************")
    print(df_clean.describe())
    print("***********************************")
    print(df_clean.info())


if __name__ == "__main__":
    main()

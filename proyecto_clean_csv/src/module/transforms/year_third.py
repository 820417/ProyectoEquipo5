import pandas as pd
from module.reports import track_changes


@track_changes
def add_year_third_column(
    df: pd.DataFrame,
    date_column: str="Transaction Date",
    output_column: str="Year third"
)-> pd.DataFrame:
    """
    Añade una columna indicando el tercio del año en el que se produce cada transacción

    El año se divide en tres periodos de cuatro meses cada uno:
        - T1: de Enero a Abril
        - T2: de Mayo a Agosto
        - T3: de Septiembre a Diciembre

    :param df: Input DataFrame.
    :type df: pd.DataFrame
    :param date_column: Nombre de la columna que contiene las fechas.
                        El Default es "Transaction Date".
    :type date_column: str
    :param output_column: Nombre de la columna que contiene los tercios del año.
                          El Default es "Year Third".
    :type output_column: str
    :raises ValueError: Si el DataFrame es None.
    :raises ValueError: Si la columna que se ha especificado no existe en el df.
    :return: Una copia del DataFrame con la nuevacolumna añadida.
    :rtype: pd.DataFrame
    """
    if df is None:
        raise ValueError("El DataFrame no se puede encontrar")

    if date_column not in df.columns:
        raise ValueError(f"Column '{date_column}' not found in DataFrame")

    df=df.copy()

    months = df[date_column].dt.month

    year_third_numeric = ((months - 1) // 4 + 1)

    df[output_column] = year_third_numeric.map({1: "T1", 2:"T2", 3:"T3"})

    return df

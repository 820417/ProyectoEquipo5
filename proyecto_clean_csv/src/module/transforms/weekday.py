import pandas as pd

from module.reports import track_changes


@track_changes
def add_weekday_column(
    df: pd.DataFrame,
    date_column: str= "Transaction Date",
    weekday_column: str="Weekday"
)-> pd.DataFrame:
    """
    Añade una columna indicando el nombre del día de la semana de cada fecha de transacción
    (e.g., Monday, Tuesday, etc.).

    :param df: Input DataFrame.
    :type df: pd.DataFrame
    :param date_column: Nombre de la columna que contiene las fechas.
                        El Default es "Transaction Date".
    :type date_column: str
    :param weekday_column: Nombre de la nueva columna añadida al df.
                           El Default es "Weekday".
    :type weekday_column: str
    :raises ValueError: Si la columna que se especifíca no existe en el df.
    :return: DataFrame con la columna nueva añadida.
    :rtype: pd.DataFrame
    """
    if date_column not in df.columns:
        raise ValueError(f"Column '{date_column}' not found in DataFrame")

    df=df.copy()

    df[weekday_column]=df[date_column].dt.day_name()

    return df

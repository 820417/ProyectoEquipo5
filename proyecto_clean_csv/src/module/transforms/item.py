import pandas as pd
from module.reports import track_changes
from module.data_models.schema import ITEM_TO_CATEGORY

@track_changes
def add_category_column(
    df: pd.DataFrame,
    item_column: str="Item",
    category_column: str = "Category",
    default_category: str = "unknown",
) -> pd.DataFrame:
    """

    Añade una columna de categoria (food/drink) en fución del producto vendido (Item)

    :param df: Input DataFrame
    :type df: pd.DataFrame
    :param item_column: Nombre de la columna que contiene el Item/Nombre del producto
    :type item_column: str
    :param category_column: Nombre de la columna añadida
    :type category_column: str
    :param default_category:Categoria que se le asigna a un producto no identificado en el .map
    :type default_category: str
    :return: DataFrame con la nueva columna de categoria
    :rtype: pd.DataFrame
    """
    if item_column not in df.columns:
        raise ValueError(f"Column '{item_column}' not found in DataFrame")

    df=df.copy()

    df[category_column] = df[item_column].map(ITEM_TO_CATEGORY).fillna(default_category)

    return df

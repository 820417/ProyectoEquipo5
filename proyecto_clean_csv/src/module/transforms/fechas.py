import pandas as pd
from module.reports import track_changes
import math

@track_changes
def tercio_del_año(df: pd.DataFrame, columna_fecha: str="Transaction Date", columna_salida: str="Tercio del año")-> pd.DataFrame:
    """
   Añadimos una columna que contiene el tercio del año segun la fecha e la que se ha dado la transacción
   Los tercios los clasificamos así:
   T1=enero-abril, T2=meyo-agosto, T3=septiembre-diciembre
   He supuesto que en este punto todas las fechas son válidas
    """
    if df is None:
        raise ValueError("El DataFrame no se puede encontrar")
    
    if columna_fecha not in df.columns:
        raise ValueError(f"La columna '{columna_fecha}' no se encunetra en el DataFrame")
   
    df=df.copy()

    df[columna_fecha]=pd.to_datetime(df[columna_fecha])

    meses=df[columna_fecha].dt.month

    tercio_del_año=math.ceil(meses/4)

    df["Tercio del año"]=tercio_del_año.map({1: "T1", 2:"T2", 3:"T3"})
    
from pathlib import Path
import pandas as pd

def csv_exporter(_self, df: pd.DataFrame) -> None:
    """
    Genera un archivo CSV limpio a partir del DataFrame procesado.
    
    :param df: DataFrame limpio a exportar
    """

    generated_dir = _self._base_dir / "generated"
    generated_dir.mkdir(exist_ok=True)

    filename = f"{_self.name}_clean.csv"
    output_path = generated_dir / filename

    df.to_csv(output_path, index=False)
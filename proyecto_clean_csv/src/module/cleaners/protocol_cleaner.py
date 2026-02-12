from typing import Protocol

import pandas as pd


class DataCleaner(Protocol):
    """Contrato: cualquier cosa con método clean(DataFrame, list[str] | None = None) → DataFrame."""

    def clean(self, df: pd.DataFrame, columns: list[str] | None = None) -> pd.DataFrame: ...

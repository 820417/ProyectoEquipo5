from typing import Any, Protocol

import pandas as pd


class Validator(Protocol):
    def validate(self, df: pd.DataFrame, config: dict[str, Any]) -> dict[str, Any]:
        ...

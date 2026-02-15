from typing import Any, Protocol

import pandas as pd


class Validator(Protocol):
    def validate(self, df: pd.DataFrame) -> dict[str, Any]:
        ...

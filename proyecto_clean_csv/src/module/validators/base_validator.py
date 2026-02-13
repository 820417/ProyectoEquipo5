from typing import Any, Dict, Protocol
import pandas as pd

class Validator(Protocol):
    def validate(self, df: pd.DataFrame) -> Dict[str, Any]:
        ...
from typing import Any, Dict
import pandas as pd
from abc import ABC, abstractmethod

class Validator:

    @abstractmethod
    def validate(self, df: pd.DataFrame) -> Dict[str, Any]:
        pass
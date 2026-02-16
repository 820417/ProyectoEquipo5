import logging
from pathlib import Path


def setup_logging(log_level: str, log_file:str)-> None:
    """Configuración del logging con un nivel específico (log_level) y un output file (log_file)."""
    numeric_level=getattr(logging, log_level.upper(), None)

    if not isinstance(numeric_level, int):
        raise ValueError(f"El log_level es inválido: {log_level}")

    log_path=Path(__file__).resolve().parent / log_file

    logging.basicConfig(
        level=numeric_level,
        format ="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

from pathlib import Path
import logging

from src.module.pipelines import DataPipelineOrchestrator
from src.module.reports.logging_config import setup_logging

logger= logging.getLogger(__name__)

def main():
    setup_logging("INFO", "app_log.txt")
    logger.info("Inicio del pipeline")

    BASE_DIR = Path(__file__).resolve().parent

    path = BASE_DIR / "examples" / "ventas_cafe.csv"
    config_path = BASE_DIR / "src" / "module" / "data_models" / "config.json"

    pipeline = DataPipelineOrchestrator(path, config_path)
    pipeline.run()

if __name__ == "__main__":
    main()

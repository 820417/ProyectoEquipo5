import logging
from pathlib import Path

from src.module.pipelines import DataPipelineOrchestrator
from src.module.reports.logging_config import setup_logging

logger= logging.getLogger(__name__)

def main():
    setup_logging("INFO", "app_log.txt")
    logger.info("Inicio del pipeline")

    base_dir = Path(__file__).resolve().parent

    path = base_dir / "examples" / "ventas_cafe.csv"
    config_path = base_dir / "src" / "module" / "data_models" / "config.json"

    pipeline = DataPipelineOrchestrator(path, config_path, base_dir)
    pipeline.run()

if __name__ == "__main__":
    main()

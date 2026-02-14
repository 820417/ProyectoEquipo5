import logging

from src.module.pipelines import DataPipelineOrchestrator
from src.module.reports.logging_config import setup_logging

logger= logging.getLogger(__name__)

def main():
    setup_logging("INFO", "app_logs.txt")
    logger.info("Inicio del pipeline")

def main():
    path = "examples/ventas_cafe.csv"
    config_path = "src/module/data_models/config.json"

    pipeline = DataPipelineOrchestrator(path, config_path)
    pipeline.run()

if __name__ == "__main__":
    main()

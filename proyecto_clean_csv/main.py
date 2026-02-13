from src.module.pipelines import DataPipelineOrchestrator


def main():
    path = "examples/ventas_cafe.csv"
    config_path = "src/module/data_models/config.json"

    pipeline = DataPipelineOrchestrator(path, config_path)
    pipeline.run()

if __name__ == "__main__":
    main()

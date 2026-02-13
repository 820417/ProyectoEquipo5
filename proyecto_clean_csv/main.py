from src.module.pipelines import DataPipelineOrchestrator


def main():
    path = "proyecto_clean_csv/examples/ventas_cafe.csv"

    pipeline = DataPipelineOrchestrator(path)
    pipeline.run()

if __name__ == "__main__":
    main()

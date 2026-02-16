from unittest.mock import MagicMock

import pandas as pd
import pytest

from module.reports import csv_exporter


def test_csv_exporter(tmp_path):
    """Verifica que el exportador crea la carpeta, el archivo y guarda los datos correctos."""
    mock_orchestrator = MagicMock()
    mock_orchestrator._base_dir = tmp_path
    mock_orchestrator.name = "test_run"

    df_input = pd.DataFrame({"id": [1, 2], "data": ["clean_a", "clean_b"]})

    csv_exporter(mock_orchestrator, df_input)

    expected_dir = tmp_path / "generated"
    expected_file = expected_dir / "test_run_clean.csv"

    assert expected_dir.is_dir()
    assert expected_file.exists()

    df_exported = pd.read_csv(expected_file)
    pd.testing.assert_frame_equal(df_input, df_exported)


def test_csv_exporter_directory_already_exists(tmp_path):
    """Verifica que la función no falla si la carpeta 'generated' ya existe."""
    mock_orchestrator = MagicMock()
    mock_orchestrator._base_dir = tmp_path
    mock_orchestrator.name = "overlap"

    generated_dir = tmp_path / "generated"
    generated_dir.mkdir()

    df_input = pd.DataFrame({"col": [1]})

    csv_exporter(mock_orchestrator, df_input)

    assert (generated_dir / "overlap_clean.csv").exists()

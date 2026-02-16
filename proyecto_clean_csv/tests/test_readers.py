from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest

from module.read.csv_reader_selector import SIZE_THRESHOLD, get_csv_reader
from module.read.reader import ReaderCSVGenerator, ReaderCSVPandas


# Fixture (csv de ejemplo)
@pytest.fixture
def fixture_csv(tmp_path: Path) -> Path:
    file_path = tmp_path / "test.csv"
    file_path.write_text(
        "Transaction Id, Quantity, Transaction Date\n"
        "TXN_3160411,5,2010-06-11\n"
        "TXN_2064365,3,1987-06-24\n",
        encoding="utf-8",
    )
    return file_path


@pytest.mark.parametrize(
    "reader_class",
    [ReaderCSVPandas, ReaderCSVGenerator],
)
def test_read_csv_valid(reader_class, fixture_csv):
    reader = reader_class()

    df = reader.read(str(fixture_csv))

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert df.iloc[0]["Transaction Id"] == "TXN_3160411"


@pytest.mark.parametrize(
    "reader_class",
    [ReaderCSVPandas, ReaderCSVGenerator],
)
def test_read_csv_not_found(reader_class):
    reader = reader_class()

    with pytest.raises(FileNotFoundError):
        reader.read("invalid_file.csv")

def test_csv_reader_selector_pandas():
    with patch("os.path.getsize", return_value=SIZE_THRESHOLD - 1):
        reader = get_csv_reader("dummy.csv")

        assert isinstance(reader, ReaderCSVPandas)

def test_csv_reader_selector_generator():
    with patch("os.path.getsize", return_value=SIZE_THRESHOLD + 1):
        reader = get_csv_reader("dummy.csv")

        assert isinstance(reader, ReaderCSVGenerator)

import numpy as np
import pandas as pd
import pytest

from module.cleaners import (
    apply_schema_types,
    drop_null_rows,
    fill_null_values,
    impute_amounts,
    remove_duplicate_rows,
)


def test_remove_duplicate_rows_keep_first():
    df = pd.DataFrame(
        {
            "Transaction ID": ["1", "2", "2", "3"],
            "Value": ["A", "B", "C", "D"],
        }
    )

    df_clean = remove_duplicate_rows(df, columns=["Transaction ID"], keep="first")

    assert len(df_clean) == 3
    assert df_clean["Value"].tolist() == ["A", "B", "D"]


def test_remove_duplicate_rows_keep_last():
    df = pd.DataFrame(
        {
            "Transaction ID": ["1", "2", "2", "3"],
            "Value": ["A", "B", "C", "D"],
        }
    )

    df_clean = remove_duplicate_rows(df, columns=["Transaction ID"], keep="last")

    assert len(df_clean) == 3
    assert df_clean["Value"].tolist() == ["A", "C", "D"]


def test_fill_null_values_specific_columns():
    df = pd.DataFrame(
        {
            "Category": ["Food", None, "Drink"],
            "Payment": ["Cash", None, "Card"],
        }
    )

    df_clean = fill_null_values(df, columns=["Category"], fill_value="NO_PROPORCIONADO")

    assert df_clean["Category"].tolist() == ["Food", "NO_PROPORCIONADO", "Drink"]
    assert pd.isna(df_clean["Payment"][1])


def test_drop_null_rows_specific_columns():
    df = pd.DataFrame(
        {
            "Critical_Col": ["A", None, "C", "D"],
            "Optional_Col": ["X", "Y", None, "W"],
        }
    )

    df_clean = drop_null_rows(df, columns=["Critical_Col"])

    assert len(df_clean) == 3
    assert df_clean["Critical_Col"].tolist() == ["A", "C", "D"]


def test_apply_schema_types():
    df = pd.DataFrame(
        {
            "Date_Col": ["2023-01-01", "invalid_date"],
            "Int_Col": ["10", "invalid_int"],
            "Float_Col": ["20.5", "invalid_float"],
            "Normal_Col": ["Texto", "Texto"],
        }
    )

    column_types = {"Date_Col": "datetime", "Int_Col": "Int64", "Float_Col": "Float64"}

    error_report = {
        "Date_Col": ["TYPE_ERROR"],
        "Int_Col": ["TYPE_ERROR"],
        "Float_Col": ["TYPE_ERROR"],
    }

    df_clean = apply_schema_types(df, column_types, error_report)

    assert pd.api.types.is_datetime64_any_dtype(df_clean["Date_Col"])
    assert df_clean["Int_Col"].dtype == "Int64"
    assert df_clean["Float_Col"].dtype == "Float64"

    assert pd.isna(df_clean["Date_Col"][1])
    assert pd.isna(df_clean["Int_Col"][1])
    assert pd.isna(df_clean["Float_Col"][1])


@pytest.mark.parametrize(
    "quantity, price, total, expected_quantity, expected_price, expected_total",
    [
        # Falta Total Spent (Quantity * Price)
        (2.0, 5.0, np.nan, 2.0, 5.0, 10.0),
        # Falta Quantity (Total / Price)
        (np.nan, 5.0, 20.0, 4.0, 5.0, 20.0),
        # Falta Price Per Unit (Total / Quantity)
        (3.0, np.nan, 15.0, 3.0, 5.0, 15.0),
    ],
)
def test_impute_amounts_calculations(
    quantity, price, total, expected_quantity, expected_price, expected_total
):
    df = pd.DataFrame(
        {
            "Quantity": [quantity],
            "Price Per Unit": [price],
            "Total Spent": [total],
        }
    )

    df_clean = impute_amounts(df)

    assert df_clean["Quantity"][0] == expected_quantity
    assert df_clean["Price Per Unit"][0] == expected_price
    assert df_clean["Total Spent"][0] == expected_total

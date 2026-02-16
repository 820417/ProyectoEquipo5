import pandas as pd
import pytest

from module.transforms.item import add_category_column
from module.transforms.weekday import add_weekday_column
from module.transforms.year_third import add_year_third_column

#add_weekday_column

def test_add_week_column_creates_weekday_column():
    df = pd.DataFrame(
        {"Transaction Date": pd.to_datetime(["2026-02-02", "2026-02-03"])}
    )

    out = add_weekday_column(df)

    assert "Weekday" in out.columns
    assert out.loc[0, "Weekday"] == "Monday"
    assert out.loc[1, "Weekday"] == "Tuesday"

def test_add_weekday_raises_if_date_time_missing():
    df = pd.DataFrame(
        {"Otro": pd.to_datetime(["2023-09-08"])}
    )
    with pytest.raises(ValueError, match="Column 'Transaction Date' not found in DataFrame"):
        add_weekday_column(df)

#add_category_column

def test_add_category_column_maps_food_and_drink():
    df = pd.DataFrame({"Item": ["Coffee", "Cake", "Tea", "Sandwich"]})

    out = add_category_column(df)

    assert "Category" in out.columns
    assert out["Category"].tolist() == ["drink", "food", "drink", "food"]

def test_add_category_column_unknown_items_default_to_unknown():
    df = pd.DataFrame({"Item": ["Coffee", "Muffin"]})  # Muffin no está en el mapping

    out = add_category_column(df)

    assert out.loc[0, "Category"] == "drink"
    assert out.loc[1, "Category"] == "unknown"

def test_add_category_column_raises_if_item_column_missing():
    df = pd.DataFrame({"Other": ["Coffee"]})

    with pytest.raises(ValueError, match="Column 'Item' not found in DataFrame"):
        add_category_column(df)

def test_add_category_column_allows_custom_column_names():
    df = pd.DataFrame({"Product": ["Coffee", "Cake"]})

    out = add_category_column(df, item_column="Product", category_column="Product Category")

    assert "Product Category" in out.columns
    assert out["Product Category"].tolist() == ["drink", "food"]

#add_year_third column

@pytest.mark.parametrize(
    "date_str, expected",
    [
        ("2023-01-01", "T1"),
        ("2023-04-30", "T1"),
        ("2023-05-01", "T2"),
        ("2023-08-31", "T2"),
        ("2023-09-01", "T3"),
        ("2023-12-31", "T3"),
    ],
)
def test_add_year_third_column_correct_labels(date_str, expected):
    df = pd.DataFrame({"Transaction Date": pd.to_datetime([date_str])})

    out = add_year_third_column(df)

    assert "Year third" in out.columns
    assert out.loc[0, "Year third"] == expected

def test_add_year_third_column_raises_if_date_column_missing():
    df = pd.DataFrame({"Other": pd.to_datetime(["2023-01-01"])})

    with pytest.raises(ValueError, match="Column 'Transaction Date' not found in DataFrame"):
        add_year_third_column(df)

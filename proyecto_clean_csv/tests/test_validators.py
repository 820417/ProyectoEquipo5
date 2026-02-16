import pandas as pd
import pytest

from module.data_models.schema import (
    DUPLICATED_VALUES_ERROR,
    NULL_VALUES_ERROR,
    TRANSACTION_ID,
    TYPE_ERROR,
)
from module.validators.specific_validators import (
    DuplicateValidator,
    NullValidator,
    TypeValidator,
)


# NullValidator
def test_null_validator_no_nulls():
    df = pd.DataFrame({
        "a": [1, 2, 3],
        "b": ["x", "y", "z"]
    })

    validator = NullValidator()
    errors = validator.validate(df)

    assert errors == {}


def test_null_validator_nulls():
    df = pd.DataFrame({
        "a": [1, None, 3],
        "b": ["4", "5", "6"],
        "c": ["x", "y", None]
    })

    validator = NullValidator()
    errors = validator.validate(df)

    assert "a" in errors
    assert "c" in errors
    assert NULL_VALUES_ERROR in errors["a"]
    assert NULL_VALUES_ERROR in errors["c"]

# DuplicateValidator
def test_duplicate_validator_no_duplicates():
    df = pd.DataFrame({
        TRANSACTION_ID: ["1", "2", "3"]
    })

    validator = DuplicateValidator()
    errors = validator.validate(df)

    assert errors == {}


def test_duplicate_validator_duplicates():
    df = pd.DataFrame({
        TRANSACTION_ID: ["1", "2", "2"]
    })

    validator = DuplicateValidator()
    errors = validator.validate(df)

    assert TRANSACTION_ID in errors
    assert DUPLICATED_VALUES_ERROR in errors[TRANSACTION_ID]


# TypeValidator
@pytest.mark.parametrize(
    "data",
    [
        ({"Quantity": ["1", "2", "3"]}),
        ({"Price Per Unit": ["10.5", "20.0", "30"]}),
        ({"Transaction Date": ["1987-06-24", "2026-02-15"]}),
        ({"Quantity": ["1", "2"], "Price Per Unit": ["10.5", "20.0"]}),
    ]
)
def test_type_validator_valid(data):
    df = pd.DataFrame(data)
    validator = TypeValidator()

    errors = validator.validate(df)

    assert errors == {}


@pytest.mark.parametrize(
    "data, valid, error_columns",
    [
        ({"Transaction ID": ["TXN_3051279", "str"]}, True, []),
        ({"Quantity": ["1", "str", "3"]}, False, ["Quantity"]),
        ({"Price Per Unit": ["10.5", "str"]}, False, ["Price Per Unit"]),
        ({"Total Spent": ["20.4", "str"]}, False, ["Total Spent"]),
        ({"Transaction Date": ["1987-06-24", "str"]}, False, ["Transaction Date"])
    ]
)
def test_type_validator_invalid(data, valid, error_columns):
    df = pd.DataFrame(data)
    validator = TypeValidator()

    errors = validator.validate(df)

    if valid:
        assert errors == {}
    else:
        for col in error_columns:
            assert col in errors
            assert TYPE_ERROR in errors[col]


TRANSACTION_ID="Transaction ID"

DUPLICATED_VALUES_ERROR = "DUPLICATED_VALUES"
NULL_VALUES_ERROR = "NULL_VALUES"
TYPE_ERROR = "TYPE_ERROR"

COLUMN_TYPES = {
    "Transaction ID": "str",
    "Item": "str",
    "Quantity": "int",
    "Price Per Unit": "float",
    "Total Spent": "float",
    "Payment Method": "str",
    "Location": "str",
    "Transaction Date": "datetime"
}

CRITICAL_COLUMNS = [
    TRANSACTION_ID,
    "Item",
    "Quantity",
    "Price Per Unit",
    "Total Spent",
    "Transaction Date"
]

NUMERIC_COLUMNS = [
    "Quantity",
    "Price Per Unit",
    "Total Spent"
]

"""Tests for clean_silwood_trees.py.

Run from the project root with:
    python3 code/test_silwood_trees.py

Successful assertions produce no output. An AssertionError indicates a failed test.
"""

import tempfile
from pathlib import Path

import clean_silwood_trees as cleaner
from clean_silwood_trees import (
    process_records,
    summarise_oaks,
    validate_record,
)


# A complete, valid record is the starting point for most tests.
good_row = {
    "record_id": "ST001",
    "location": "Silwood Bottom",
    "genus": "Quercus",
    "species": "robur",
    "distance_m": "25",
    "angle_degrees": "45",
}


# 1. A good record is accepted and numeric values are written as decimal text.
record, reasons = validate_record(good_row, 2, set())
assert record == {
    "record_id": "ST001",
    "location": "Silwood Bottom",
    "genus": "Quercus",
    "species": "robur",
    "distance_m": "25.0",
    "angle_degrees": "45.0",
}
assert reasons == []


# 2. Surrounding spaces and letter case are normalised to canonical spellings.
messy_row = dict(
    good_row,
    location="  nAsH's FiElD  ",
    genus="  qUeRcUs  ",
    species="  RoBuR  ",
)
record, reasons = validate_record(messy_row, 2, set())
assert record["location"] == "Nash's Field"
assert record["genus"] == "Quercus"
assert record["species"] == "robur"
assert reasons == []


# 3. Blank values produce the exact corresponding missing-field reason.
for field_name in good_row:
    row = dict(good_row, **{field_name: "   "})
    record, reasons = validate_record(row, 2, set())
    assert record is None
    assert reasons == [f"missing {field_name}"]


# 4. Missing dictionary keys are handled as missing fields too.
for field_name in good_row:
    row = dict(good_row)
    del row[field_name]
    record, reasons = validate_record(row, 2, set())
    assert record is None
    assert reasons == [f"missing {field_name}"]


# 5. Record IDs must start with uppercase ST and have exactly three digits.
for bad_id in ["st001", "ST01", "ST0001", "TREE001"]:
    record, reasons = validate_record(
        dict(good_row, record_id=bad_id), 2, set()
    )
    assert record is None
    assert reasons == ["invalid record_id"]

# Surrounding whitespace around a valid ID is allowed.
record, reasons = validate_record(
    dict(good_row, record_id="  ST001  "), 2, set()
)
assert record["record_id"] == "ST001"
assert reasons == []


# 6. Unrecognised locations, genera and species are rejected, not guessed.
record, reasons = validate_record(
    dict(good_row, location="Silwood Botom"), 2, set()
)
assert record is None
assert reasons == ["invalid location"]

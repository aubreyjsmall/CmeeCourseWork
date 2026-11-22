#!/usr/bin/env python3
# Author: Aubrey <a.small26@imperial.ac.uk>
# script: test_silwood_trees.py
# Desc: Tests for clean_silwood_trees.py
# Date: Nov 2026
"""Tests for clean_silwood_trees.py.

Run from the project root:
    python3 code/test_silwood_trees.py

Tests use small made-up records and temporary files. The raw survey is never
modified. Two tests run the real cleaner, which writes to the git-ignored
results/ directory.
"""

import csv
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CODE_DIR))

import clean_silwood_trees as cst

ROOT = cst.PROJECT_ROOT
RESULTS = cst.RESULTS_DIR
RAW = cst.INPUT_PATH
OUTPUT_NAMES = [
    "silwood_trees_clean.csv",
    "silwood_tree_issues.csv",
    "oak_species_counts.csv",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def rec(**overrides):
    """A valid raw record, with any fields overridden."""
    row = {
        "record_id": "ST001",
        "location": "Silwood Bottom",
        "genus": "Quercus",
        "species": "robur",
        "distance_m": "12.5",
        "angle_degrees": "30",
    }
    row.update(overrides)
    return row


def clean_rec(genus, species):
    """An already-cleaned record, as passed to summarise_oaks."""
    return {
        "record_id": "ST001",
        "location": "Manor House",
        "genus": genus,
        "species": species,
        "distance_m": "10.0",
        "angle_degrees": "30.0",
    }


def check(row, accepted=None):
    """Call validate_record with a fresh set of accepted IDs by default."""
    return cst.validate_record(row, 2, set() if accepted is None else accepted)


def reasons_for(**overrides):
    """Assert a record is rejected and return its reasons."""
    clean, reasons = check(rec(**overrides))
    assert clean is None, f"expected rejection for {overrides}"
    return reasons


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot_results():
    if not RESULTS.exists():
        return {}
    return {p.name: sha(p) for p in RESULTS.glob("*")}


def read_csv_rows(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


# ---------------------------------------------------------------------------
# validate_record: accepted and cleaned
# ---------------------------------------------------------------------------

def test_valid_record_accepted():
    clean, reasons = check(rec())
    assert reasons == []
    assert clean == {
        "record_id": "ST001",
        "location": "Silwood Bottom",
        "genus": "Quercus",
        "species": "robur",
        "distance_m": "12.5",
        "angle_degrees": "30.0",
    }


def test_text_cleaning():
    clean, reasons = check(rec(
        record_id=" ST007 ",
        location="  silwood BOTTOM ",
        genus=" QUERCUS ",
        species=" Robur ",
        distance_m=" 12.5 ",
        angle_degrees=" 30 ",
    ))
    assert reasons == []
    assert clean["record_id"] == "ST007"
    assert clean["location"] == "Silwood Bottom"
    assert clean["genus"] == "Quercus" and clean["species"] == "robur"
    assert clean["distance_m"] == "12.5" and clean["angle_degrees"] == "30.0"


def test_nashs_field_spelling():
    clean, _ = check(rec(location="NASH'S FIELD"))
    assert clean["location"] == "Nash's Field"


# ---------------------------------------------------------------------------
# Missing and unrecognised values
# ---------------------------------------------------------------------------

def test_missing_values():
    for field in cst.INPUT_FIELDS:
        for blank in ("", "   ", None):
            assert reasons_for(**{field: blank}) == [f"missing {field}"], (field, blank)


def test_unrecognised_values():
    assert reasons_for(record_id="st001") == ["invalid record_id"]  # case matters
    assert reasons_for(record_id="ST1") == ["invalid record_id"]
    assert reasons_for(record_id="XX001") == ["invalid record_id"]
    assert reasons_for(location="Nowhere") == ["invalid location"]
    assert reasons_for(genus="Pinus") == ["invalid genus"]
    assert reasons_for(species="alba") == ["invalid species"]


def test_invalid_genus_species_pair():
    assert reasons_for(genus="Acer", species="robur") == [
        "invalid genus/species combination"
    ]


# ---------------------------------------------------------------------------
# Measurements
# ---------------------------------------------------------------------------

def test_invalid_numbers():
    for bad in ("abc", "nan", "inf", "-inf", "12,5"):
        assert reasons_for(distance_m=bad) == ["invalid distance_m"], bad
        assert reasons_for(angle_degrees=bad) == ["invalid angle_degrees"], bad


def test_distance_boundaries():
    for bad in ("0", "-1", "100.1"):
        assert reasons_for(distance_m=bad) == ["distance_m out of range"], bad
    for good in ("0.1", "100"):
        assert check(rec(distance_m=good))[0] is not None, good


def test_angle_boundaries():
    for bad in ("0", "-5", "90", "95"):
        assert reasons_for(angle_degrees=bad) == ["angle_degrees out of range"], bad
    for good in ("0.1", "89.9"):
        assert check(rec(angle_degrees=good))[0] is not None, good


def test_scientific_notation_and_curly_apostrophe():
    assert check(rec(distance_m="1e2"))[0] is not None  # equals 100, allowed
    assert reasons_for(distance_m="1e3") == ["distance_m out of range"]
    # A curly apostrophe is not corrected: the location is rejected.
    assert reasons_for(location="Nash\u2019s Field") == ["invalid location"]


# ---------------------------------------------------------------------------
# Multiple problems and short rows
# ---------------------------------------------------------------------------

def test_multiple_problems_all_reported_in_order():
    assert reasons_for(location="", genus="Oak", distance_m="abc") == [
        "missing location",
        "invalid genus",
        "invalid distance_m",
    ]


def test_short_row_missing_columns():
    row = {"record_id": "ST001", "location": "Manor House"}
    clean, reasons = check(row)
    assert clean is None
    assert "missing genus" in reasons and "missing distance_m" in reasons


# ---------------------------------------------------------------------------
# Duplicates and process_records
# ---------------------------------------------------------------------------

def test_duplicate_id_rejected_by_validate():
    clean, reasons = check(rec(), accepted={"ST001"})
    assert clean is None and reasons == ["duplicate record_id"]


def test_duplicates_first_kept_and_rejected_row_does_not_reserve_id():
    rows = [
        rec(),                                         # row 2: accepted
        rec(species="petraea"),                        # row 3: duplicate of ST001
        rec(record_id="ST002", angle_degrees="95"),    # row 4: rejected
        rec(record_id="ST002"),                        # row 5: same ID, now accepted
    ]
    clean, issues = cst.process_records(rows)
    assert [r["record_id"] for r in clean] == ["ST001", "ST002"]
    assert clean[0]["species"] == "robur"              # first copy kept
    assert [i["source_row"] for i in issues] == ["3", "4"]
    assert issues[0]["reasons"] == "duplicate record_id"
    assert issues[1]["reasons"] == "angle_degrees out of range"


def test_id_whitespace_still_counts_as_duplicate():
    clean, issues = cst.process_records([rec(), rec(record_id=" ST001 ")])
    assert len(clean) == 1 and issues[0]["reasons"] == "duplicate record_id"


def test_issue_reasons_joined_with_semicolons():
    _, issues = cst.process_records([rec(location="", genus="Oak")])
    assert issues == [{
        "source_row": "2",
        "record_id": "ST001",
        "reasons": "missing location; invalid genus",
    }]


def test_every_row_in_exactly_one_place():
    rows = [rec(), rec(), rec(record_id="ST002", genus=""), rec(record_id="ST003")]
    clean, issues = cst.process_records(rows)
    assert len(clean) + len(issues) == len(rows)


def test_clean_records_sorted_by_id():
    clean, _ = cst.process_records([rec(record_id="ST003"), rec(record_id="ST001")])
    assert [r["record_id"] for r in clean] == ["ST001", "ST003"]


def test_empty_input():
    assert cst.process_records([]) == ([], [])
    assert cst.summarise_oaks([]) == []


def test_all_rows_invalid_gives_no_oaks():
    clean, issues = cst.process_records([rec(genus="Pinus"), rec(record_id="bad")])
    assert clean == [] and len(issues) == 2
    assert cst.summarise_oaks(clean) == []


# ---------------------------------------------------------------------------
# summarise_oaks
# ---------------------------------------------------------------------------

def test_oak_summary_exact_names_and_non_oaks():
    records = [
        clean_rec("Quercus", "robur"),
        clean_rec("Quercus", "robur"),
        clean_rec("Quercus", "petraea"),
        clean_rec("Acer", "pseudoplatanus"),
    ]
    assert cst.summarise_oaks(records) == [
        {"species": "petraea", "count": "1"},
        {"species": "robur", "count": "2"},
    ]


def test_oak_summary_near_match_not_counted():
    # A near-match genus is not counted by the summary itself...
    assert cst.summarise_oaks([clean_rec("Quercu", "robur")]) == []
    # ...and is rejected before it can reach the summary.
    clean, issues = cst.process_records([rec(genus="Querkus")])
    assert clean == [] and issues[0]["reasons"] == "invalid genus"
    assert cst.summarise_oaks(clean) == []


def test_oak_summary_no_oaks():
    assert cst.summarise_oaks([clean_rec("Fagus", "sylvatica")]) == []


# ---------------------------------------------------------------------------
# End-to-end flow
# ---------------------------------------------------------------------------

def test_end_to_end_flow_valid_and_invalid():
    """One valid and one invalid record travel through the whole pipeline."""
    valid = rec(record_id="ST001", species="robur")
    invalid = rec(record_id="ST002", species="petraea", angle_degrees="95")

    clean, issues = cst.process_records([valid, invalid])

    # The valid record is accepted and the invalid one reported.
    assert [r["record_id"] for r in clean] == ["ST001"]
    assert [i["record_id"] for i in issues] == ["ST002"]
    assert issues[0]["source_row"] == "3"
    assert issues[0]["reasons"] == "angle_degrees out of range"

    # Only the cleaned record reaches the oak summary. If the invalid petraea
    # leaked through, "petraea" would appear here.
    assert cst.summarise_oaks(clean) == [{"species": "robur", "count": "1"}]


def test_main_writes_expected_outputs():
    """Run main() on a 5-row survey and check all three output files."""
    lines = [
        ",".join(cst.INPUT_FIELDS),
        "ST001,Silwood Bottom,Quercus,robur,10,30",       # row 2: accepted
        "ST002,manor house,QUERCUS,Petraea,20,45",        # row 3: accepted (cleaned)
        "ST003,Reactor Wood,Quercus,robur,0,30",          # row 4: distance out of range
        "ST001,Reactor Wood,Fagus,sylvatica,5,10",        # row 5: duplicate ID
        "ST004,Nash's Field,Acer,pseudoplatanus,8,60",    # row 6: accepted, not an oak
    ]
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        survey = tmp / "survey.csv"
        survey.write_text("\n".join(lines) + "\n", encoding="utf-8")

        # Point main() at the small survey and a temporary results folder.
        orig_load, orig_results = cst.load_records, cst.RESULTS_DIR
        cst.load_records = lambda: orig_load(survey)
        cst.RESULTS_DIR = tmp / "results"
        try:
            cst.main()
        finally:
            cst.load_records, cst.RESULTS_DIR = orig_load, orig_results

        out = tmp / "results"
        clean = read_csv_rows(out / "silwood_trees_clean.csv")
        issues = read_csv_rows(out / "silwood_tree_issues.csv")
        oaks = read_csv_rows(out / "oak_species_counts.csv")

        assert [r["record_id"] for r in clean] == ["ST001", "ST002", "ST004"]
        assert clean[1]["location"] == "Manor House"
        assert clean[1]["species"] == "petraea"
        assert issues == [
            {"source_row": "4", "record_id": "ST003",
             "reasons": "distance_m out of range"},
            {"source_row": "5", "record_id": "ST001",
             "reasons": "duplicate record_id"},
        ]
        assert oaks == [
            {"species": "petraea", "count": "1"},
            {"species": "robur", "count": "1"},
        ]


# ---------------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------------

def test_load_records_rejects_wrong_columns():
    with tempfile.TemporaryDirectory() as tmp:
        bad = Path(tmp) / "bad.csv"
        bad.write_text("id,place\n1,x\n", encoding="utf-8")
        try:
            cst.load_records(bad)
        except ValueError:
            return
        raise AssertionError("expected ValueError for wrong header")


def test_load_records_reads_small_file():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "ok.csv"
        path.write_text(
            ",".join(cst.INPUT_FIELDS)
            + "\nST001,Manor House,Acer,pseudoplatanus,5,20\n",
            encoding="utf-8",
        )
        rows = cst.load_records(path)
        assert len(rows) == 1 and rows[0]["record_id"] == "ST001"


def test_header_only_survey_gives_empty_outputs():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "header_only.csv"
        path.write_text(",".join(cst.INPUT_FIELDS) + "\n", encoding="utf-8")
        rows = cst.load_records(path)
        assert rows == []
        clean, issues = cst.process_records(rows)
        assert (clean, issues) == ([], [])
        assert cst.summarise_oaks(clean) == []


# ---------------------------------------------------------------------------
# Whole-program behaviour
# ---------------------------------------------------------------------------

def test_import_has_no_side_effects():
    before = snapshot_results()
    out = subprocess.run(
        [sys.executable, "-c", "import clean_silwood_trees"],
        cwd=CODE_DIR, capture_output=True, text=True,
    )
    assert out.returncode == 0, out.stderr
    assert out.stdout == "" and snapshot_results() == before


def test_running_twice_gives_same_results_and_raw_data_unchanged():
    raw_before = sha(RAW)
    snapshots = []
    for _ in range(2):
        subprocess.run(
            [sys.executable, str(CODE_DIR / "clean_silwood_trees.py")],
            cwd=ROOT, check=True, capture_output=True,
        )
        snapshots.append({name: sha(RESULTS / name) for name in OUTPUT_NAMES})
    assert snapshots[0] == snapshots[1]
    assert sha(RAW) == raw_before


def test_real_survey_accounting():
    rows = cst.load_records()
    clean, issues = cst.process_records(rows)
    assert len(clean) + len(issues) == len(rows)
    ids = [r["record_id"] for r in clean]
    assert len(ids) == len(set(ids)), "duplicate IDs in clean output"


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def main():
    tests = [(name, func) for name, func in sorted(globals().items())
             if name.startswith("test_") and callable(func)]
    failed = 0
    for name, func in tests:
        try:
            func()
            print(f"PASS {name}")
        except Exception as exc:
            failed += 1
            print(f"FAIL {name}: {type(exc).__name__}: {exc}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
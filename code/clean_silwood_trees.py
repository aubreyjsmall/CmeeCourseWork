#!/usr/bin/env python3
"""Validate and clean the synthetic Silwood tree survey."""

from __future__ import annotations

import csv
import math
import re
from pathlib import Path
from typing import Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "silwood_trees_raw.csv"
RESULTS_DIR = PROJECT_ROOT / "results"

INPUT_FIELDS = [
    "record_id",
    "location",
    "genus",
    "species",
    "distance_m",
    "angle_degrees",
]
ISSUE_FIELDS = ["source_row", "record_id", "reasons"]
OAK_COUNT_FIELDS = ["species", "count"]

# Each key is a lower-case lookup value; each value is the required spelling.
LOCATIONS = {
    "silwood bottom": "Silwood Bottom",
    "nash's field": "Nash's Field",
    "manor house": "Manor House",
    "reactor wood": "Reactor Wood",
}

GENERA = {
    "quercus": "Quercus",
    "acer": "Acer",
    "betula": "Betula",
    "fagus": "Fagus",
    "fraxinus": "Fraxinus",
}

SPECIES = {
    "robur": "robur",
    "petraea": "petraea",
    "pseudoplatanus": "pseudoplatanus",
    "pendula": "pendula",
    "sylvatica": "sylvatica",
    "excelsior": "excelsior",
}

TAXON_PAIRS = [
    ("Quercus", "robur"),
    ("Quercus", "petraea"),
    ("Acer", "pseudoplatanus"),
    ("Betula", "pendula"),
    ("Fagus", "sylvatica"),
    ("Fraxinus", "excelsior"),
]

def load_records(path: Path = INPUT_PATH) -> list[dict[str, str]]:
    """Read the survey and check its column names."""
    with path.open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames != INPUT_FIELDS:
            raise ValueError(
                f"Expected columns {INPUT_FIELDS}, found {reader.fieldnames}"
            )
        return list(reader)

def parse_number(
    value: str | None,
    field_name: str,
    reasons: list[str],
) -> float | None:
    """Convert a numeric field and record missing or invalid values."""
    if value is None or not value.strip():
        reasons.append(f"missing {field_name}")
        return None

    try:
        number = float(value.strip())
    except ValueError:
        reasons.append(f"invalid {field_name}")
        return None

    if not math.isfinite(number):
        reasons.append(f"invalid {field_name}")
        return None

    return number

def validate_record(
    row: dict[str, str],
    source_row: int,
    accepted_ids: set[str],
) -> tuple[dict[str, str] | None, list[str]]:
    """Clean one record, or return the reasons it cannot be used."""
    reasons = []

    # Trim the ID without changing case; the required prefix is uppercase ST.
    record_id = (row.get("record_id") or "").strip()
    if not record_id:
        reasons.append("missing record_id")
    elif not re.match(r"^ST[0-9]{3}$", record_id):
        reasons.append("invalid record_id")
    elif record_id in accepted_ids:
        reasons.append("duplicate record_id")

    # Match location names without regard to case, then use canonical spelling.
    location_text = (row.get("location") or "").strip()
    location = LOCATIONS.get(location_text.lower())
    if not location_text:
        reasons.append("missing location")
    elif location is None:
        reasons.append("invalid location")

    # Validate the genus and species separately before checking the pair.
    genus_text = (row.get("genus") or "").strip()
    genus = GENERA.get(genus_text.lower())
    if not genus_text:
        reasons.append("missing genus")
    elif genus is None:
        reasons.append("invalid genus")

    species_text = (row.get("species") or "").strip()
    species = SPECIES.get(species_text.lower())
    if not species_text:
        reasons.append("missing species")
    elif species is None:
        reasons.append("invalid species")

    if genus is not None and species is not None:
        if (genus, species) not in TAXON_PAIRS:
            reasons.append("invalid genus/species combination")

    # A value must convert to a finite number before a range check is applied.
    distance = parse_number(row.get("distance_m"), "distance_m", reasons)
    if distance is not None and not (0 < distance <= 100):
        reasons.append("distance_m out of range")

    angle = parse_number(row.get("angle_degrees"), "angle_degrees", reasons)
    if angle is not None and not (0 < angle < 90):
        reasons.append("angle_degrees out of range")

    # Return no cleaned record if any problem was found.
    if reasons:
        return None, reasons

    cleaned_record = {
        "record_id": record_id,
        "location": location,
        "genus": genus,
        "species": species,
        "distance_m": str(distance),
        "angle_degrees": str(angle),
    }
    return cleaned_record, reasons

def process_records(
    rows: Iterable[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Sort records into accepted rows and issue reports."""
    clean_records = []
    issues = []
    accepted_ids = set()

    # The first data row is line 2 because line 1 contains the CSV header.
    for source_row, row in enumerate(rows, start=2):
        clean_record, reasons = validate_record(row, source_row, accepted_ids)

        if clean_record is None:
            issues.append(
                {
                    "source_row": str(source_row),
                    "record_id": (row.get("record_id") or "").strip(),
                    "reasons": "; ".join(reasons),
                }
            )
        else:
            clean_records.append(clean_record)
            # Only accepted records reserve an ID; invalid rows do not.
            accepted_ids.add(clean_record["record_id"])

    clean_records.sort(key=lambda record: record["record_id"])
    return clean_records, issues

def summarise_oaks(
    clean_records: Iterable[dict[str, str]],
) -> list[dict[str, str]]:
    """Count accepted oak records by species."""
    counts = {}

    for record in clean_records:
        if record["genus"] == "Quercus":
            species = record["species"]
            if species in counts:
                counts[species] = counts[species] + 1
            else:
                counts[species] = 1

    oak_counts = []
    for species in sorted(counts):
        oak_counts.append(
            {"species": species, "count": str(counts[species])}
        )

    return oak_counts


def write_csv(
    path: Path,
    fieldnames: list[str],
    rows: Iterable[dict[str, str]],
) -> None:
    """Write rows to a CSV file, replacing an older copy."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as destination:
        writer = csv.DictWriter(destination, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    """Clean the survey and write the three result files."""
    clean_records, issues = process_records(load_records())
    oak_counts = summarise_oaks(clean_records)

    write_csv(
        RESULTS_DIR / "silwood_trees_clean.csv",
        INPUT_FIELDS,
        clean_records,
    )
    write_csv(
        RESULTS_DIR / "silwood_tree_issues.csv",
        ISSUE_FIELDS,
        issues,
    )
    write_csv(
        RESULTS_DIR / "oak_species_counts.csv",
        OAK_COUNT_FIELDS,
        oak_counts,
    )


if __name__ == "__main__":
    main()
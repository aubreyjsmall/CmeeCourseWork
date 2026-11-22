#!/bin/bash
# Author: Aubrey <a.small26@imperial.ac.uk>
# script: run_get_TreeHeight.sh
# Desc: run get_TreeHeight.R from the project root, stopping if it fails
# Arguments: optional CSV path (default: data/trees.csv)
# Usage: bash code/run_get_TreeHeight.sh [csv_file]

# set -e exits immediately if any command fails, so an R error
# gives this script a non-zero exit status too
set -e

if [[ $# -gt 1 ]]; then
    printf "usage: %s [csv_file]\n" "$(basename "$0")" >&2
    exit 2
fi

input="${1:-data/trees.csv}"

Rscript code/get_TreeHeight.R "$input"


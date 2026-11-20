#!/bin/bash
# Run get_TreeHeight.R on data/trees.csv from the project root.
# Stops if the command fails.

#set -e makes the script exit immediately if any command returns a non-zero status, which covers the “stop if the command fails” requirement.
set -e

Rscript code/get_TreeHeight.R data/trees.csv
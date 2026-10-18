#!/bin/bash
# Author: Aubrey <a.small26@imperial.ac.uk>
# script: tabtocsv.sh
# Desc: substitute the tabs in the files with commas
#       saves the output into a .csv file
# Arguments: 1-> Tab-delimited file
# Date: Oct 2026


#Accept exactly one readable tab-delimited input file. 
#check if the number of arguments is not equal to 1

if [[ $# -ne 1 ]]; then
    printf "usage: %s <tab-delimited-file>\n" "$0" >&2
    exit 2
fi

#check if the file exists and is readable
if [[ ! -f "$1" || ! -r "$1" ]]; then
    printf "error: file '%s' does not exist or is not readable\n" "$1" >&2
    exit 1
fi

echo "Creating a comma delimited version of $1 ..."

#Leave the input unchanged. Write the result to ../results/<input-filename>.csv. Make the results folder if it isn't there

script_dir=$(dirname "$0")
results_dir="$script_dir/../results"

mkdir -p "$results_dir"

output="$results_dir/$(basename "$1").csv"

#convert tabs to commas and write to the output file and check if the conversion was successful

tr '\t' ',' < "$1" > "$output"
if [[ $? -ne 0 ]]; then
    printf 'Error: conversion failed\n' >&2
    exit 1
fi

printf 'Done! Output is in %s\n' "$output"
exit 


#!/bin/bash
# Author: Aubrey <a.small26@imperial.ac.uk>
# script: csvtospace.sh
# Desc: substitute the commas in the files with spaces
#       saves the output into a .csv file
# Arguments: 1-> Comma-delimited file
# Date: Oct 2026

#Accept exactly one readable CSV input path 
#check if the number of arguments is not equal to 1

if [[ $# -ne 1 ]]; then
    printf "usage: %s <csv_file>\n" "$0" >&2
    exit 2
fi

#check if the file exists and is readable
if [[ ! -f "$1" || ! -r "$1" ]]; then
    printf "error: file '%s' does not exist or is not readable\n" "$1" >&2
    exit 1
fi

#Leave the input unchanged. Write the result to ../results/<input-filename>.txt. Make the results folder if it isn't there

mkdir -p ../results

output="../results/$(basename "$1").txt"

#convert commas to spaces and write to the output file and check if the conversion was successful

tr ',' ' ' < "$1" > "$output"
if [[ $? -ne 0 ]]; then
    printf 'Error: conversion failed\n' >&2
    exit 1
fi

printf 'Done! Output is in %s\n' "$output"
exit 
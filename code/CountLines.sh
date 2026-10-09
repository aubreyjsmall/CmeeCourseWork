#!/bin/bash
# Author: Aubrey <a.small26@imperial.ac.uk>
# script: CountLines.sh
# Desc: Count the number of lines in a file
# Arguments: 1-> File to count lines in
# Date: Oct 2026

NumLines= 'wc -l < "$1"'
echo "The file $1 has $NumLines lines"
echo



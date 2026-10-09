#!/bin/bash
# Author: Aubrey <a.small26@imperial.ac.uk>
# script: ConcatenateTwoFiles.sh
# Desc: Concatenate two files and save the output into a new file
# Arguments: 1-> First file
#            2-> Second file       
# Date: Oct 2026

cat "$1" > "$3" # create a new file and write the contents of the first file into it
cat "$2" >> "$3" # append the contents of the second file into the new file
echo "Merged File is" # echo a message to the terminal 
cat "$3" # read the new file and print it to the terminal



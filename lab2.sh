#!/bin/bash

# ------------------------------------
# SETUP
# Please do not modify this section.

# bash command-line arguments are accessible as $0 (the bash script), $1, etc.
echo "Running" $0 "on" $1

input_file=$1
ulimit -v 1000000   # limit the virtual memory to 1000000 bytes = 1 MB
# ------------------------------------

# ------------------------------------
# STUDENT CODE
# Please replace this section with your solution.

# Example: This will parse the first 20 lines of $input_file and write the results
# to both STDOUT and to a file called example.csv.

echo -e "Here is an example of streaming data into a python function:\n\n"

# you can use \ break up a long sequence of unix pipes onto separate lines...
# just make sure that "\" is the last character on each line

head -n 5 $input_file | \
python -c 'import lab2; lab2.example_function()' | \
tee example.csv

echo -e "\n\nAbove results were also written to a file called example.csv"
# ------------------------------------
#!/usr/bin/env bash

echo See the Open Academic Graph web site:
echo https://www.aminer.org/oag2019
echo " "

etl () {
    echo " "
    echo Processing $1
    [[ -f "$1.csv" ]] && { echo "$1.csv already exists, so skipping"; return 0 ; }
    [[ -f "$1.zip" ]] || { wget -c https://academicgraphv2.blob.core.windows.net/oag/$2/author/$1.zip ; }
    [[ -f "$1.zip" ]] || { echo ".zip file does not exist after download attempt"; exit 1 ; }
    time python3 etl_open_academic_graph.py --min-pub 10 --min-citation 10 --require-latin --remove-replacement $1.zip $1.csv || exit 1
}
etl aminer_authors_0 aminer
etl aminer_authors_1 aminer
etl aminer_authors_2 aminer
etl aminer_authors_3 aminer
etl mag_authors_0 mag
etl mag_authors_1 mag
etl mag_authors_2 mag

# compress
time 7z a -mm=Deflate -mfb=258 -mpass=15 -r open_academic_graph_v2.zip aminer_*csv mag_*csv

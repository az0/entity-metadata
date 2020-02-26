#!/usr/bin/python3

#
# Copyright (C) 2019 by Compassion International.  All rights reserved.
# License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
# This is free software: you are free to change and redistribute it.
# There is NO WARRANTY, to the extent permitted by law.


"""
ETL North Carolina voter registration files

1. Read state-wide tab-delimited file
2. Narrow down the columns
3. Output all counties to a single CSV file

Source data available here:
https://www.ncsbe.gov/data-stats/other-election-related-data
http://dl.ncsbe.gov/data/ncvoter_Statewide.zip
"""


import glob
import sys
import pandas as pd


def groupby(df, col):
    gb = df.groupby(col)[[col]].count()
    print(gb)


def go():
    """The main loop"""
    if not len(sys.argv) == 3:
        print('As arguments pass (1) the state-wide NC voter registration file and (2) the output .csv filename.')
        print('Example: python3 %s ncvoter_Statewide.txt nc.csv' % sys.argv[0])
        sys.exit(1)
    in_fn = sys.argv[1]
    out_fn = sys.argv[2]
    usecols = [3, 9, 10, 11, 12, 25, 26, 28]
    print('Reading tab-delimited file: %s' % in_fn)
    df = pd.read_csv(in_fn, sep='\t', usecols=usecols)
    print('Row count: {:,}'.format(df.shape[0]))
    groupby(df, 'status_cd')
    groupby(df, 'race_code')
    groupby(df, 'ethnic_code')
    groupby(df, 'gender_code')
    print('Writing to CSV file: %s' % out_fn)
    df.to_csv(out_fn, index=False)


go()

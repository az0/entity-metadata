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
https://www.ncsbe.gov/results-data/voter-registration-data#current-data
https://s3.amazonaws.com/dl.ncsbe.gov/data/ncvoter_Statewide.zip
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
    usecols = ['county_id','voter_reg_num','ncid','status_cd','last_name','first_name','middle_name','name_suffix_lbl','race_code','ethnic_code','gender_code']
    print(f'Reading tab-delimited file: {in_fn}')
    df = pd.read_csv(in_fn, sep='\t', usecols=usecols, encoding='iso-8859-1')
    print('Row count: {:,}'.format(df.shape[0]))
    groupby(df, 'status_cd')
    groupby(df, 'race_code')
    groupby(df, 'ethnic_code')
    groupby(df, 'gender_code')
    print(f'Writing to CSV file: {out_fn}')
    df.to_csv(out_fn, index=False) # encoding defaults to utf-8


go()

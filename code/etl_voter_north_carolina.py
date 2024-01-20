#!/usr/bin/python3

#
# Copyright (C) 2019,2024 by Compassion International.  All rights reserved.
# License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
# This is free software: you are free to change and redistribute it.
# There is NO WARRANTY, to the extent permitted by law.


"""
ETL North Carolina voter registration files

1. Read state-wide tab-delimited file
2. Narrow down the columns
3. Output all counties to a single CSV file


# Source data available here

https://www.ncsbe.gov/results-data/voter-registration-data#current-data
https://s3.amazonaws.com/dl.ncsbe.gov/data/ncvoter_Statewide.zip
https://dl.ncsbe.gov/index.html?prefix=data/Snapshots/


# Layout change

Compared to latest (January 2024) the 2005 snapshot (VR_20051125.txt) has different names
name_suffix_lbl:name_sufx_cd
gender_code:sex_code
middle_name:midl_name

This program standardizes them to the new names.


# Encoding

Documentation for snapshot states UTF-16-LE, but it is not.

https://s3.amazonaws.com/dl.ncsbe.gov/data/Snapshots/layout_VR_Snapshot.txt

"""


import glob
import sys
import pandas as pd

FILE_ENCODING = 'iso-8859-1'
FILE_SEP = '\t'
COL_NAME_MAP = {
    'sex_code': 'gender_code',
    'name_sufx_cd': 'name_suffix_lbl',
    'midl_name': 'middle_name'
}


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
    want_cols = ['county_id', 'voter_reg_num', 'ncid', 'status_cd', 'name_prefx_cd', 'last_name', 'first_name',
                 'middle_name', 'midl_name', 'name_suffix_lbl', 'name_sufx_cd', 'race_code', 'ethnic_code', 'gender_code', 'sex_code']
    print(f'Reading tab-delimited file: {in_fn}')
    df_header = pd.read_csv(in_fn, sep=FILE_SEP,
                            encoding=FILE_ENCODING, nrows=0)
    has_cols = df_header.columns
    use_cols = list(set(want_cols) & set(has_cols))
    missing_cols = list(set(want_cols) - set(has_cols))
    print(f'File has columns: {has_cols}')
    print(f'Columns are missing: {missing_cols}')
    print(f'Using columns: {use_cols}')

    import csv
    df = pd.read_csv(in_fn, sep=FILE_SEP, encoding=FILE_ENCODING,
                     usecols=use_cols, on_bad_lines='warn', quoting=csv.QUOTE_NONE)
    print('Row count: {:,}'.format(df.shape[0]))

    print('Trimming whitespace')
    string_cols = df.select_dtypes(include=['object'])
    string_cols = string_cols.apply(lambda x: x.str.strip())
    df[string_cols.columns] = string_cols

    print('Standardizing the names of columns')
    for old_col, new_col in COL_NAME_MAP.items():
        if old_col in has_cols:
            print(f'Renaming {old_col} to {new_col}')
            df.rename(columns={old_col: new_col}, inplace=True)

    groupby(df, 'status_cd')
    groupby(df, 'race_code')
    groupby(df, 'ethnic_code')
    groupby(df, 'gender_code')
    print(f'Writing to CSV file: {out_fn}')
    df.to_csv(out_fn, index=False)  # encoding defaults to utf-8


go()

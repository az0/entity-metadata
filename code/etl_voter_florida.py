#!/usr/bin/python3

#
# Copyright (C) 2019 by Compassion International.  All rights reserved.
# License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
# This is free software: you are free to change and redistribute it.
# There is NO WARRANTY, to the extent permitted by law.


"""
ETL Florida voter registration files

1. Read each tab-delimited file
2. Narrow down the columns
3. Output all counties to a single CSV file

Source data available here:
https://dos.fl.gov/elections/data-statistics/voter-registration-statistics/voter-extract-request/
"""


import glob
import re
import sys


import pandas as pd
import numpy as np


def read_one(in_fn):
    """Read a single file"""
    print('Reading Florida tab-delimited file: %s' % in_fn)
    col_names = ['id', 'last', 'suffix', 'first', 'middle',
                 'gender', 'race', 'birth_date_str', 'reg_date_str', 'status']
    df = pd.read_csv(in_fn, sep='\t', usecols=[
                     1, 2, 3, 4, 5, 19, 20, 21, 22, 28], names=col_names, index_col=None)
    return df


def clean(df_all):
    print('head()')
    print(df_all.head())

    print('Summarizing nominal variables')
    print(df_all.gender.value_counts())
    print(df_all.race.value_counts())
    print(df_all.suffix.value_counts())
    print(df_all.status.value_counts())

    print('Standardizing suffix')
    df_all.loc[df_all.suffix.isin(['JR', 'Jr', 'JR.']), 'suffix'] = 'Jr.'
    df_all.loc[df_all.suffix.isin(['SR', 'Sr', 'SR.']), 'suffix'] = 'Sr.'
    df_all.loc[df_all.suffix.isin(['2ND']), 'suffix'] = 'II'
    df_all.loc[df_all.suffix.isin(['3RD']), 'suffix'] = 'III'
    df_all.loc[df_all.suffix.isin(['MRS', 'DR.', 'REV']), 'suffix'] = np.nan
    print(df_all.suffix.value_counts())

    print('Standardizing date')
    df_all['reg_date'] = pd.to_datetime(
        df_all['reg_date_str'], format='%m/%d/%Y', errors='coerce')
    print(f'Registration date range is {df_all.reg_date.min()} to {df_all.reg_date.max()}')
    df_all['birth_date'] = pd.to_datetime(
        df_all['birth_date_str'], format='%m/%d/%Y', errors='coerce')
    print(f'Birth date range is {df_all.birth_date.min()} to {df_all.birth_date.max()}')
    df_all['birth_month'] = df_all.birth_date.values.astype('datetime64[M]')

    print('Cleaning up whitespace')
    df_all['first'] = df_all['first'].str.strip()
    df_all['middle'] = df_all['middle'].str.strip()
    df_all['last'] = df_all['last'].str.strip()

    print('Marking exceptions')
    idx_valid_suffix = (df_all.suffix.isin(
        ['Jr.', 'Sr.', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', '*']) | df_all.suffix.isna())

    def is_valid_name(row):
        for p in ['first', 'middle', 'last']:
            value = row[p]
            if value is np.nan:
                continue
            if value.lower() in ['*', '(none)', 'none']:
                return False
            if re.search(r'[^a-zA-Z_\'\-\s\.\*\/(\)\"]', value):
                # non-name characters such as digits, slash
                return False
        for p in ['first', 'last']:
            if not row[p]:
                return False
        return True
    idx_valid_name = df_all.apply(lambda row: is_valid_name(row), axis=1)
    # Oldest living person in United States was born 1905
    # https://en.wikipedia.org/wiki/List_of_the_oldest_living_people
    idx_exception = ~idx_valid_suffix | \
        ~idx_valid_name | \
        (df_all.reg_date < pd.Timestamp(1910, 1, 1)) | \
        (df_all.birth_date < pd.Timestamp(1905, 1, 1)) | \
        (df_all.birth_date > df_all.reg_date)
    print(f'Exception count: {idx_exception.sum():,} ({100.0*idx_exception.sum()/df_all.shape[0]:.2f})%')
    df_all.loc[idx_exception, 'exception'] = 1

    df_all = df_all.sort_values(by=['last', 'birth_date', 'first'])
    df_all.drop(['reg_date_str', 'birth_date_str',
                 'birth_date'], axis=1, inplace=True)
    return df_all


def go():
    """The main loop"""
    if not len(sys.argv) == 3:
        print('As arguments pass (1) the directory of the Florida .txt files and (2) the output .csv filename.')
        print('Example: python3 %s /tmp/florida/ /tmp/fl.csv' % sys.argv[0])
        sys.exit(1)
    in_dir = sys.argv[1]
    out_fn = sys.argv[2]
    print('in_dir=', in_dir)
    print('out_fn=', out_fn)
    df_list = []
    for in_fn in glob.glob(in_dir+'/*.txt'):
        df = read_one(in_fn)
        df_list.append(df)
    print('Combining files')
    df_all = pd.concat(df_list, axis=0, ignore_index=True)

    df_all = clean(df_all)

    print('Writing to CSV file: %s' % out_fn)
    df_all.to_csv(out_fn, index=False, float_format='%.0f')


go()

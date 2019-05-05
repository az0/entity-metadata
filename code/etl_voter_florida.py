#!/usr/bin/python3

#
# Copyright (C) 2019 by Andrew Ziem.  All rights reserved.
# License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
# This is free software: you are free to change and redistribute it.
# There is NO WARRANTY, to the extent permitted by law.


"""
ETL Florida voter registration files

1. Read each tab-delimited file
2. Narrow down the columns
3. Output all counties to a single CSV file

Source data available here:
http://flvoters.com/downloads.html
"""


import glob
import sys
import pandas as pd


def read_one(in_fn):
    """Read a single file"""
    print('Reading Florida tab-delimited file: %s' % in_fn)
    col_names = ['last', 'suffix', 'first', 'middle',
                 'gender', 'race', 'reg_date', 'status']
    df = pd.read_csv(in_fn, sep='\t', usecols=[
                     2, 3, 4, 5, 19, 20, 22, 28], names=col_names, index_col=None)
    return df


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
    print('head()')
    print(df_all.head())
    print('Writing to CSV file: %s' % out_fn)
    df_all.to_csv(out_fn, index=False)


go()

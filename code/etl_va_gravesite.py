#!/usr/bin/python3

#
# Copyright (C) 2019 by Andrew Ziem.  All rights reserved.
# License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
# This is free software: you are free to change and redistribute it.
# There is NO WARRANTY, to the extent permitted by law.

"""
Extract names from data set of gravesite locations of veterans and beneficiaries

https://catalog.data.gov/dataset?res_format=CSV&organization=va-gov&q=gravesite&_bureauCode_limit=0

"""

import os
import urllib.request
import glob
import pandas as pd
import numpy as np
import sys


us_states = ('Alabama',
             'Alaska',
             'Arizona',
             'Arkansas',
             'California',
             'Colorado',
             'Connecticut',
             'Delaware',
             'Florida',
             'Georgia',
             'Hawaii',
             'Idaho',
             'Illinois',
             'Indiana',
             'Iowa',
             'Kansas',
             'Kentucky',
             'Louisiana',
             'Maine',
             'Maryland',
             'Massachusetts',
             'Michigan',
             'Minnesota',
             'Mississippi',
             'Missouri',
             'Montana',
             'Nebraska',
             'Nevada',
             'New Hampshire',
             'New Jersey',
             'New Mexico',
             'New York',
             'North Carolina',
             'North Dakota',
             'Ohio',
             'Oklahoma',
             'Oregon',
             'Pennsylvania',
             'Rhode Island',
             'South Carolina',
             'South Dakota',
             'Tennessee',
             'Texas',
             'Utah',
             'Vermont',
             'Virginia',
             'Washington',
             'West Virginia',
             'Wisconsin',
             'Wyoming')


# not case sensitive
URL_TPL = 'https://www.va.gov/digitalstrategy//cemdata/%sstatefiles/ngl_%s.csv'


def download_state(vintage, us_state_name):
    us_state_id = us_state_name.lower().replace(' ', '_')
    url = URL_TPL % (vintage, us_state_id)
    csv_fn = os.path.expanduser('~/.cache/va_gravesite_%s.csv' % us_state_id)
    print('%s -> %s ' % (url, csv_fn))
    try:
        g = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        print('HTTPError')
        return
    with open(csv_fn, 'b+w') as f:
        f.write(g.read())


def download_all(vintage):
    for us_state in us_states:
        download_state(us_state)


def etl():
    fnames = glob.glob(os.path.expanduser('~/.cache/va_gravesite_*.csv'))
    if not fnames:
        print('No files found: ~/.cache/va_gravesite_*.csv')
        print('Try --download')
        sys.exit(1)
    df_list = []
    for fname in fnames:
        print(fname)
        try:
            df_state = pd.read_csv(fname, low_memory=False, index_col=False,
                                   dtype={'zip': np.str})
        except Exception as e:
            print(e)
        else:
            df_state = df_state[['d_first_name', 'd_mid_name',
                                 'd_last_name', 'd_birth_date', 'd_death_date', 'state', 'zip']]
            print(df_state.head())
            df_list.append(df_state)

    df_all = pd.concat(df_list, ignore_index=True)
    print('Total column count: %d' % df_all.shape[0])
    assert pd.to_numeric(df_all.zip).min() >= 501
    assert pd.to_numeric(df_all.zip).max() <= 99999
    df_all.sort_values(by=['state', 'zip', 'd_last_name',
                           'd_first_name', 'd_mid_name', 'd_death_date'], inplace=True)
    df_all.to_csv('va_gravesite_all.csv', index=False)


def go():
    import argparse
    parser = argparse.ArgumentParser(
        description='Extract names from Veterans gravesites')
    parser.add_argument(
        '--download', help='download from va.gov to ~/.cache', action='store_true')
    parser.add_argument(
        '--etl', help='extract from all files, transform, and load into single file', action='store_true')
    parser.add_argument('--vintage', help='nov2018, feb2019, may2019, etc.')
    args = parser.parse_args()
    if not (args.download or args.etl):
        parser.error('No action requested, see --help')
    if args.download:
        download_all(args.vintage)
    if args.etl:
        etl()


if __name__ == '__main__':
    go()

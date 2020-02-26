#!/usr/bin/python3

#
# Copyright (C) 2019 by Compassion International.  All rights reserved.
# License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
# This is free software: you are free to change and redistribute it.
# There is NO WARRANTY, to the extent permitted by law.

"""
Download public records data from MicroPact license rosters.

"""

# Not yet added:
# Colorado Division of Real Estate
# https://apps.colorado.gov/dre/licensing/Lookup/GenerateRoster.aspx

import csv
import os

import pandas as pd


def download_set(code, url_template, roster_ids, dl_dir):
    """Download a set of files for which mapping is unknown"""
    for roster_id in roster_ids:
        url = url_template % roster_id
        local_fn = '%s-%d.csv' % (code, roster_id)
        local_fn_full = os.path.join(dl_dir, local_fn)
        print("%s --> %s" % (url, local_fn))
        if os.path.exists(local_fn_full):
            print('     Already exists')
        else:
            import urllib.request
            try:
                urllib.request.urlretrieve(url, local_fn_full)
            except Exception as e:
                print(e)
                continue
        try:
            csvdf = pd.read_csv(local_fn_full, low_memory=False)
        except Exception as e:
            print(e)
            continue
        record_count = csvdf.shape[0]
        roster = {'code': code, 'url_template': url_template,
                  'roster_id': roster_id, 'record_count': record_count}
        roster_writer.writerow(roster)

        for col_i in range(0, csvdf.shape[1]):
            col_name = csvdf.columns.values[col_i]
            print('%s %s %s (%d)' % (code, roster_id, col_name, col_i))
            if record_count >= 1:
                sample1 = csvdf.ix[0, col_i]
            else:
                sample1 = ''
            if record_count >= 2:
                sample2 = csvdf.ix[1, col_i]
            else:
                sample2 = ''
            cols = {'code': code, 'roster_id': roster_id, 'name': col_name,
                    'sample1': sample1, 'sample2': sample2, 'map_to': None}
            cols_writer.writerow(cols)


def download_sets(dl_dir):
    """Download sets for exploration"""

    roster_fn = os.path.join(dl_dir, 'roster.csv')
    roster_f = open(roster_fn, 'w')
    roster_fieldnames = ('code', 'url_template', 'roster_id', 'record_count')
    global roster_writer
    roster_writer = csv.DictWriter(roster_f, fieldnames=roster_fieldnames)
    roster_writer.writeheader()

    cols_fn = os.path.join(dl_dir, 'roster_column.csv')
    cols_f = open(cols_fn, 'w')
    cols_fieldnames = ('code', 'roster_id', 'name',
                       'sample1', 'sample2', 'map_to')
    global cols_writer
    cols_writer = csv.DictWriter(cols_f, fieldnames=cols_fieldnames)
    cols_writer.writeheader()

    # Colorado Department of Regulatory Services
    # https://apps.colorado.gov/dora/licensing/Lookup/GenerateRoster.aspx
    co_dora_roster_ids = [
        1593310,
        1593311,
        1593317,
        1593364,
        1593365,
        1593366,
        1593367,
        1593368,
        1593370,
        1593371,
        1593372,
        1593373,
        1593374,
        1593375,
        1593376,
        1593377,
        1593378,
        1593379,
        1593380,
        1593381,
        1593382,
        1593383,
        1593384,
        1593385,
        1593386,
        1593387,
        1593388,
        1593389,
        1593390,
        1593391,
        1593392,
        1593393,
        1593394,
        1593395,
        1593396,
        1593397,
        1593398,
        1593399,
        1593400,
        1593401,
        1593402,
        1593403,
        1593404,
        1593405,
        1593406,
        1593407,
        1593408,
        1593409,
        1593410,
        1593411,
        1593412,
        1593413,
        1593414,
        1593415,
        1593416,
        1593417,
        1593418,
        1593419,
        1593420,
        1593421,
        1593422,
        1593423,
        1593424,
        1593425,
        1593426,
        1593427,
        1593428,
        1593429,
        1593430,
        1593431,
        1593432,
        1593433,
        1593434,
        1593435,
        1593436,
        1593437,
        1593438,
        1593439,
        1593440,
        1593441,
        1593442,
        1593443,
        1593444,
        1593445,
        1593446,
        1593447,
        1593448,
        1593449,
        1593450,
        1593451,
        1593452,
        1593453,
        1593454,
        1593455,
        1593456,
        1593457,
        1593458,
        1593459,
        1593460,
        1593461,
        1593462,
        1593463,
        1593464,
        1593465]

    download_set('co_dora', "https://apps.colorado.gov/dora/licensing/Lookup/FileDownload.aspx?Idnt=%d&Type=Comma",
                 co_dora_roster_ids, dl_dir)

    # Colorado Department of Education
    # https://apps.colorado.gov/cde/licensing/Lookup/GenerateRoster.aspx
    co_cde_roster_ids = [
        1878,
        1879,
        1880,
        1881,
        1882,
        1883,
        1884,
        1885]

    download_set('co_cde', "https://apps.colorado.gov/cde/licensing/Lookup/FileDownload.aspx?Idnt=%d&Type=Comma",
                 co_cde_roster_ids, dl_dir)

    # Oregon
    # https://orea.elicense.irondata.com/Lookup/GenerateRoster.aspx
    or_real_roster_ids = [68119,
                          68120,
                          68121,
                          68122,
                          68123,
                          68124,
                          68125,
                          68126,
                          68127,
                          68128]
    # 68129
    download_set('or_real', 'https://orea.elicense.irondata.com/Lookup/FileDownload.aspx?Idnt=%s&Type=Comma',
                 or_real_roster_ids, dl_dir)

    # Kansas OSBC
    # https://online.osbckansas.org/Lookup/GenerateRoster.aspx
    ks_osbc_roster_ids = [209293,
                          209294,
                          209295,
                          209296,
                          209297,
                          209298,
                          209299,
                          209300,
                          209301]
    download_set('ks_osbc', 'https://online.osbckansas.org/Lookup/FileDownload.aspx?Idnt=%s&Type=Comma',
                 ks_osbc_roster_ids, dl_dir)

    # CT
    # https://www.elicense.ct.gov/Lookup/GenerateRoster.aspx
    ct_roster_ids = [822837, 822838, 822839, 822840, 822841, 822842, 822843, 822844, 822845, 822846, 822847, 822848, 822849, 822850, 822851, 822852, 822853, 822854, 822855, 822856, 822857, 822858, 822859, 822860, 822861, 822862, 822863, 822864, 822865, 822866, 822867, 822868, 822869, 822870, 822871, 822872, 822873, 822874, 822875, 822876, 822877, 822878, 822879, 822880, 822881, 822882, 822883, 822884, 822885, 822886, 822887, 822888, 822889, 822890, 822891, 822892, 822893, 822894, 822895, 822896, 822897, 822898, 822899, 822900, 822901, 822902, 822903, 822904, 822905, 822906, 822907, 822908, 822909, 822910, 822911, 822912, 822913, 822914, 822915, 822916, 822917, 822918, 822919, 822920, 822921, 822922, 822923, 822924, 822925, 822926, 822927, 822928, 822929, 822930, 822931, 822932, 822933, 822934,
                     822935, 822936, 822937, 822938, 822939, 822940, 822941, 822942, 822943, 822944, 822945, 822946, 822947, 822948, 822949, 822950, 822951, 822952, 822953, 822954, 822955, 822956, 822957, 822958, 822959, 822960, 822961, 822962, 822963, 822964, 822965, 822966, 822967, 822968, 822969, 822970, 822971, 822972, 822973, 822974, 822975, 822976, 822977, 822978, 822979, 822980, 822981, 822982, 822983, 822984, 822985, 822986, 822987, 822988, 822989, 822990, 822991, 822992, 822993, 822994, 822995, 822996, 822997, 822998, 822999, 823000, 823001, 823002, 823003, 823004, 823005, 823006, 823007, 823008, 823009, 823010, 823011, 823012, 823013, 823014, 823015, 823016, 823017, 823018, 823019, 823020, 823021, 823022, 823023, 823024, 823025, 823026, 823027, 823028, 823029, 823030, 823031, 823032, 823033, 823034]
    download_set('ct', 'https://www.elicense.ct.gov/Lookup/FileDownload.aspx?Idnt=%s&Type=Comma',
                 ct_roster_ids, dl_dir)

    # Ohio Division of Financial Institutions
    # https://elicense2-secure.com.ohio.gov/Lookup/GenerateRoster.aspx
    oh_dfi_roster_ids = [16395]

    download_set('oh_dfi', "https://elicense2-secure.com.ohio.gov/Lookup/FileDownload.aspx?Idnt=%s&aType=Comma",
                 oh_dfi_roster_ids, dl_dir)

    # Ohio Real Estate and Profession Licensing
    # https://elicense3.com.ohio.gov/Lookup/DownloadRoster.aspx
    oh_real_roster_ids = [55506]
    download_set('oh_real', "https://elicense3.com.ohio.gov/Lookup/FileDownload.aspx?Idnt=%s&aType=Comma",
                 oh_real_roster_ids, dl_dir)

    # OCILB - Ohio Construction Industry Licensing Board Rosters
    # https://elicense4.com.ohio.gov/Lookup/GenerateRoster.aspx
    oh_ocilb_roster_ids = [29940]
    download_set('oh_ocilb', "https://elicense4.com.ohio.gov/Lookup/FileDownload.aspx?Idnt=%s&aType=Comma",
                 oh_ocilb_roster_ids, dl_dir)


def make_unique(val, seen_vals):
    if val not in seen_vals:
        return val
    for i in range(2, 20):
        new_val = '%s%d' % (val, i)
        if not new_val in seen_vals:
            return new_val
    raise RuntimeError('cannot make unique: %s' % val)


def etl_roster(dl_dir, roster_fn, roster_map):
    """ETL a single roster"""
    roster_fn = os.path.join(dl_dir, roster_fn)
    print('Processing:', roster_fn)

    # make sure every new column name is unique
    seen_vals = []
    for (i, val) in roster_map['map_to'].items():
        new_val = make_unique(val, seen_vals)
        roster_map.ix[i, 1] = new_val
        seen_vals.append(new_val)
    roster_df = pd.read_csv(roster_fn, low_memory=False)

    rename_dict = {row['name']: row['map_to']
                   for (index, row) in roster_map.iterrows()}
    roster_df = roster_df.rename(index=str, columns=rename_dict)
    drop_col = set(roster_df.columns.values) - set(seen_vals)
    roster_df.drop(drop_col, axis=1, inplace=True)
    final_col = roster_df.columns.values
    assert(len(final_col) == len(set(final_col)))

    return roster_df


def etl_all(dl_dir):
    """ETL all rosters"""
    col_fn = os.path.join(dl_dir, 'roster_column.csv')
    print('Reading file:', col_fn)
    col_df = pd.read_csv(col_fn, low_memory=False)
    print('Original column row count:', col_df.shape[0])
    col_df = col_df[col_df.map_to.notnull()]
    print('New column row count:', col_df.shape[0])
    print('Count by map_to')
    print(col_df.groupby('map_to').size())
    col_df['roster_fn'] = col_df[['code', 'roster_id']].apply(
        lambda x: '{}-{}.csv'.format(x[0], x[1]), axis=1)

    col_all = ('fn', 'full', 'first', 'middle', 'last',
               'entity', 'entity2', 'business', 'organization')
    roster_all_df = pd.DataFrame(columns=col_all)

    for roster_fn in col_df['roster_fn'].unique():
        roster_map = col_df[col_df['roster_fn'] == roster_fn][[
            'name', 'map_to']].reset_index(drop=True)
        roster_df = etl_roster(dl_dir, roster_fn, roster_map)
        roster_df['fn'] = roster_fn

        if roster_df.shape[0] > 1:
            roster_all_df = pd.concat(
                (roster_all_df, roster_df), ignore_index=True, sort=False)
        print('Row count: {:,} / {:,} (this / all)'.format(
            roster_df.shape[0], roster_all_df.shape[0]))

    roster_all_fn = os.path.join(dl_dir, 'all.csv')
    roster_all_df.to_csv(roster_all_fn, index=False)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--explore", action='store_true')
    parser.add_argument(
        "--etl", help="combine all .csv files using mapping from roster_column.csv", action='store_true')
    parser.add_argument("--dir", help="directory for .csv files", type=str)
    args = parser.parse_args()
    if args.explore:
        download_sets(args.dir)
    if args.etl:
        etl_all(args.dir)

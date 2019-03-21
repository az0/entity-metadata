#!/usr/bin/python3

#
# Copyright (C) 2019 by Andrew Ziem.  All rights reserved.
# License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
# This is free software: you are free to change and redistribute it.
# There is NO WARRANTY, to the extent permitted by law.


"""
This program ETLs the Open Library authors dump file.

The input is a tab-delimited file with JSON in one column.

The output is a simpler file, which is a CSV with basic biographical
information plus unique identifiers.

Get the dump from here
https://openlibrary.org/developers/dumps

Do not decompress the dump file.
"""


import csv
import sys
import gzip
import json


csv.field_size_limit(sys.maxsize)

# The value id_wikidata (not nested under remote_ids) is defined
# exactly once out of 6.9M records, and in that case it's redundant
# to the value nested under remote_ids. It seems to be a mistake,
# so we'll ignore it.

retain_keys = ['key', 'id_wikidata', 'entity_type', 'name', 'fuller_name', 'personal_name', 'alternate_names',
               'birth_date', 'death_date']


def process_json(j, writer):
    author = json.loads(j)
    author_retain = {}
    for retain_key in retain_keys:
        if retain_key in author:
            author_retain[retain_key] = author[retain_key]
    if 'remote_ids' in author and 'wikidata' in author['remote_ids']:
        # extract nested value
        author_retain['id_wikidata'] = author['remote_ids']['wikidata']
    if 'alternate_names' in author:
        # reformat multiple items from JSON list to pipe delimited
        author_retain['alternate_names'] = '|'.join(author['alternate_names'])
    writer.writerow(author_retain)


def go():
    if len(sys.argv) != 3:
        print(
            'Usage: %s (path to OpenLibrary authors .txt.gz) (path to output .csv)' % sys.argv[0])
        sys.exit(1)
    txt_gz_fn = sys.argv[1]
    csv_out_fn = sys.argv[2]
    with gzip.open(txt_gz_fn, 'rt') as inf:  # inf= IN File
        reader = csv.reader(inf, delimiter='\t')
        with open(csv_out_fn, 'w') as outf:
            writer = csv.DictWriter(outf, fieldnames=retain_keys)
            writer.writeheader()
            print('Processing...')
            count = 0
            for row in reader:
                process_json(row[4], writer)
                count += 1
                if (count % 10000) == 0:
                    # progress indicator
                    print('.', end='', flush=True)
    print('\nDone.')


go()

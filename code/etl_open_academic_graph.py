#!/usr/bin/python3

#
# Copyright (C) 2019 by Andrew Ziem.  All rights reserved.
# License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
# This is free software: you are free to change and redistribute it.
# There is NO WARRANTY, to the extent permitted by law.

"""
Extract names of authors and organizations from Open Academic
Graph 2019

https://www.aminer.org/oag2019

"""


import csv
import json
import sys
fieldnames = ('name', 'org', 'n_pubs', 'n_citation')


def has_latin(s):
    """Checks whether the string has any Latin characters"""
    import re
    return re.search('[a-zA-Z]', s)


def process_file(f_in, writer):
    """Process a single text file, which has one JSON per line"""
    import codecs
    for line in codecs.iterdecode(f_in, 'utf8'):
        author = json.loads(line)
        author_out = {}
        for field in fieldnames:
            if field in author:
                author_out[field] = author[field]
        if has_latin(author_out['name']):
            writer.writerow(author_out)


def go():
    """The main program"""
    import argparse
    parser = argparse.ArgumentParser(
        description='Extract person and organization names from Open Academic Graph')
    parser.add_argument(
        'zip_filename', help='input author .zip filename (not extracted)')
    parser.add_argument('csv_filename', help='output .csv filename')
    args = parser.parse_args()
    # Open the DictWriter first and once because all the embedded files
    # will be written to a single .csv file.
    with open(args.csv_filename, 'w') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        from zipfile import ZipFile
        print('Reading .zip file:', args.zip_filename)
        with ZipFile(args.zip_filename, 'r') as zf:
            # Iterate over embedded files
            for zip_fn in zf.namelist():
                print('Reading embedded file:', zip_fn)
                with zf.open(zip_fn) as f_in:
                    process_file(f_in, writer)


if __name__ == '__main__':
    go()

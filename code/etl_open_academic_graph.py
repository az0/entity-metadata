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
import re
fieldnames = ('name', 'org', 'n_pubs', 'n_citation')


def has_latin(s):
    """Checks whether the string has any Latin characters"""
    return re.search('[a-zA-Z]', s)


def process_file(f_in, writer, filter_args):
    """Process a single text file, which has one JSON per line"""
    import codecs
    for line in codecs.iterdecode(f_in, 'utf8'):
        author = json.loads(line)
        author_out = {}
        for field in fieldnames:
            if field in author:
                author_out[field] = author[field]
        if not 'n_pubs' in author_out:
            author_out['n_pubs'] = 0
        if not 'n_citation' in author_out:
            author_out['n_citation'] = 0
        if filter_args.require_latin and not has_latin(author_out['name']):
            continue
        if filter_args.min_pub > author_out['n_pubs']:
            continue
        if filter_args.min_citation > author_out['n_citation']:
            continue
        if filter_args.remove_replacement:
            if re.search('\ufffd', author['name']):
                continue
            if 'org' in author and re.search('\ufffd', author['org']):
                del author_out['org']
                continue
        writer.writerow(author_out)


def go():
    """The main program"""
    import argparse
    parser = argparse.ArgumentParser(
        description='Extract person and organization names from Open Academic Graph')
    parser.add_argument(
        'zip_filename', help='input author .zip filename (not extracted)')
    parser.add_argument(
        '--min-pub', help='keep authors with at least X publications', default=0, type=int)
    parser.add_argument(
        '--min-citation', help='keep authors with at least X citations', default=0, type=int)
    parser.add_argument(
        '--require-latin', help='keep only authors with name with at least one Latin character', action='store_true')
    parser.add_argument(
        '--remove-replacement', help='remove author names with the Unicode character FFFD', action='store_true')
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
                    process_file(f_in, writer, args)


if __name__ == '__main__':
    go()

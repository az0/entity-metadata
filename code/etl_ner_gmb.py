#!/usr/bin/python3

#
# Copyright (C) 2019 by Compassion International.  All rights reserved.
# License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
# This is free software: you are free to change and redistribute it.
# There is NO WARRANTY, to the extent permitted by law.

"""
Extract persons and organizations from annotated corpus for Named Entitity
Recognition (NER)

https://www.kaggle.com/abhinavwalia95/entity-annotated-corpus/data

"""

import pandas as pd

import csv
import sys


current_name = []
current_tag = None


def process_row(row, writer):
    global current_name
    global current_tag
    tag = row['Tag'][2:]
    if row['Tag'] in ('B-per', 'B-org'):
        current_name.append(row['Word'])
        current_tag = row['Tag'][2:]
    elif tag == current_tag:
        current_name.append(row['Word'])
    else:
        if current_name:
            joined_name = ' '.join(current_name)
            #print(current_tag, joined_name)
            writer.writerow([current_tag, joined_name])
            current_name = []
            current_tag = None


def go():
    if not 3 == len(sys.argv):
        print ('usage: %s input_file.csv output_file.csv' % (sys.argv[0]))
        sys.exit(1)
    fn_in = sys.argv[1]
    fn_out = sys.argv[2]
    ner_df = pd.read_csv(fn_in, encoding='iso-8859-1')
    print(ner_df.groupby('POS').count())
    print(ner_df.groupby('Tag').count())
    with open(fn_out, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        for index, row in ner_df.iterrows():
            process_row(row, csvwriter)


if '__main__' == __name__:
    go()

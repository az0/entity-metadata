#
# Copyright (C) 2017 by Andrew Ziem.  All rights reserved.
# License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
# This is free software: you are free to change and redistribute it.
# There is NO WARRANTY, to the extent permitted by law.

"""
Run a CSV through probablepeople to tag all rows. It's
also useful to check for tagging errors.

Tested with Python 2.7
"""

import probablepeople as pp

from collections import OrderedDict
import csv
import sys

tagged_rows = []
tags = set()
initial_keys  = []


def read(fn_in):
    global tags, tagged_rows, initial_keys 
    print 'Reading and parsing: %s' % fn_in
    with open(fn_in, 'rb') as incsvfile:
        reader = csv.DictReader(incsvfile, delimiter=',')
        counter = 0

        for row in reader:
            # stop early for development
            #if counter > 1000:
            #    break
            try:
                row['name'] = row['name'].decode('utf8')
                tagged = pp.tag(row['name'])
                # add t_ prefix to distinguish from original columns
                tagged0 = OrderedDict(('t_'+k, v) for k, v in tagged[0].viewitems())
                # add type
                tagged0['tag_type'] = tagged[1]
                # add to dictionary of input values
                row.update(tagged0)
            except pp.RepeatedLabelError:
                row['tag_type'] = 'RepeatedLabelError'
            except UnicodeEncodeError:
                #https://github.com/datamade/probablepeople/issues/54
                row['tag_type'] = 'UnicodeEncodeError'
            [tags.add(t) for t in row.keys()]
            tagged_rows.append(row)
            counter = counter + 1

    print 'Read {:,} rows'.format(counter)

    # preserve the original order of field names
    initial_keys = reader.fieldnames

def write(fn_out):
    global tags, tagged_rows, initial_keys 
    print 'Writing output: %s' % fn_out

    tags_unique = [tag for tag in tags if not tag in initial_keys]
    out_fields = initial_keys + tags_unique

    with open(fn_out, 'wb') as outcsvfile:
        writer = csv.DictWriter(outcsvfile, fieldnames=out_fields)
        writer.writeheader()
        for tagged_row in tagged_rows:
            encoded_row = {k:v.encode('utf8') for k,v in tagged_row.items()}
            writer.writerow(encoded_row)

if '__main__' == __name__:
    if not 3 == len(sys.argv):
        print ('usage: tag_csv.py input_file.csv output_file.csv')
        sys.exit(1)
    fn_in = sys.argv[1]
    fn_out = sys.argv[2]
    read(fn_in)
    write(fn_out)

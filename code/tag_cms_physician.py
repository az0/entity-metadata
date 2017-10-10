#
# Copyright (C) 2017 by Andrew Ziem.  All rights reserved.
# License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
# This is free software: you are free to change and redistribute it.
# There is NO WARRANTY, to the extent permitted by law.

"""
Run the CMS Physician data set through probablepeople
and check for errors
"""

import probablepeople as pp
import csv
from collections import OrderedDict

in_fn = '../data/cms-physician-permutation.csv'

out_fn = '../data/cms-physician-permutation-tagged.csv'

tagged_rows = []
tags = set()

print 'Reading and parsing'
with open(in_fn, 'rb') as incsvfile:
    reader = csv.DictReader(incsvfile, delimiter=',')
    counter = 0
    for row in reader:
        # stop early for development
        #if counter > 1000:
        #    break
        try:
            tagged = pp.tag(row['name'])
            # add t_ prefix to distinguish
            tagged0 = OrderedDict(('t_'+k, v) for k, v in tagged[0].viewitems())
            # add type
            tagged0['tag_type'] = tagged[1]
            # add to dictionary of input values
            row.update(tagged0)
        except pp.RepeatedLabelError:
            row['tag_type'] = 'RepeatedLabelError'
        [tags.add(t) for t in row.keys()]
        tagged_rows.append(row)
        counter = counter + 1

print 'Read {:,} rows'.format(counter)
        
print 'Writing output'
initial_keys = reader.fieldnames # preserve the original order of field names
error_keys = ['error_found_second_entity', 'error_surname', 'error_tag_type' ,'error_any']
tags_unique = [tag for tag in tags if not tag in initial_keys]
out_fields = initial_keys + tags_unique + error_keys

def check_row(row):
    # ignore the second marital prefix
    row.pop('t_SecondPrefixMarital', None)
    # second person or second corporation
    row['error_found_second_entity'] = any([k.find('Second')> -1 for k in row.keys()])
    # surname missing or different
    row['error_surname'] = 't_Surname' not in row.keys() or not row['last_name'] == row['t_Surname']
    # not a person (i.e., corporation or RepeatedLabelError)
    # Household can be OK because we added prefixes like "Mr. & Mrs."
    row['error_tag_type'] = not row['tag_type']  in ('Person', 'Household')
    # any error
    row['error_any'] = any([row[k] for k in row.keys() if k.startswith('error_')])
    return row

with open(out_fn, 'wb') as outcsvfile:
    writer = csv.DictWriter(outcsvfile, fieldnames=out_fields)
    writer.writeheader()
    for tagged_row in tagged_rows:
        checked_row = check_row(tagged_row)
        writer.writerow(checked_row)
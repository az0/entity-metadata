#
# Copyright (C) 2017 by Compassion International.  All rights reserved.
# License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
# This is free software: you are free to change and redistribute it.
# There is NO WARRANTY, to the extent permitted by law.


"""
This script reads church names from STDIN. The input format is one church name
per line. It is not a CSV, so there is neither a header nor any commas.

It output format is XML to train a model for probablepeople.

The labeling rules are not perfect, so manually check the labels.

This script works with Python 3.6.
"""

import fileinput

org_tokens = [
    'abbey',
    'baptist',
    'basilica',
    'cathedral',
    'catholic',
    'chapel',
    'church',
    'co-cathedral',
    'episcopal ',
    'evangelical ',
    'lutheran',
    'methodist',
    'mission'
    'parish',
    'parsonage',
    'universalist',
]


def label_church(s):
    labels = []
    for token in s.split(' '):
        if token.lower() in org_tokens:
            label = '<CorporationNameOrganization>%s</CorporationNameOrganization>' % token
        else:
            label = '<CorporationName>%s</CorporationName>' % token
        labels.append(label)
    label = '    <Name>%s</Name>' % ' '.join(labels)
    return label


labels = []
for line in fileinput.input():
    line = line.replace('\n', '')
    if not line.strip():
        # blank
        continue
    label = label_church(line)
    labels.append(label)

for label in labels:
    print (label)

#
# Copyright (C) 2017 by Andrew Ziem.  All rights reserved.
# License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
# This is free software: you are free to change and redistribute it.
# There is NO WARRANTY, to the extent permitted by law.


"""
This program reads in a CSV file of organizations exported from [PetScan]
(https://petscan.wmflabs.org/). Then this script looks for a column 
called "wikidata" with Wikidata IDs, and then for each entity, it looks up
metadata about the entities in Wikidata. It creates another CSV file with
this metadata.

This program works with Python 3.6.

This program is slow. Try the other one! :)
"""

# non-standard imports
from joblib import Memory
from wikidata.client import Client
import percache

# standard imports
import os.path
import sys
import tempfile

# set up cache
tmpdir = os.path.join(tempfile.gettempdir(), 'wikidata.org.percache')
cache = percache.Cache(tmpdir)

# globals
fieldnames = ['wikidata_id', 'name', 'instance_of', 'country']

# set up Wikidata client
client = Client()
p_instance_of = client.get('P31')
p_country = client.get('P17')


def get_label(e, p):
    """Get label from Wikidata"""
    r = None
    try:
        r = e[p].label
    except KeyError:
        pass
    return r


@cache
def lookup_organization(wikidata_id):
    """Look up an entity, presumed to be an organization, on Wikidata"""
    print ('lookup organization %s' % wikidata_id)
    # get entity
    entity = client.get(wikidata_id)

    # labels for entity
    labels = dict()
    labels['wikidata_id'] = wikidata_id
    labels['name'] = entity.label
    labels['instance_of'] = get_label(entity, p_instance_of)
    labels['country'] = get_label(entity, p_country)

    return labels


def main(fn_in, fn_out):
    import csv
    # The newline='' avoids blank lines between rows.
    with open(fn_out, 'w', encoding='utf-8', newline='') as csvfile_out:
        writer = csv.DictWriter(csvfile_out, fieldnames=fieldnames)
        writer.writeheader()
        with open(fn_in, encoding='utf-8') as csvfile_in:
            reader = csv.reader(csvfile_in)
            header_row = next(reader)
            wikidata_index = header_row.index('wikidata')
            for row in reader:
                wikidata_id = row[wikidata_index]
                import re
                if not wikidata_id or not re.match('Q\d+', wikidata_id):
                    # Some entries from PetScan have no ID
                    continue
                print ('read id %s' % wikidata_id)
                try:
                    labels = lookup_organization(wikidata_id)
                except KeyboardInterrupt:
                    break
                except:
                    import traceback
                    traceback.print_exc()
                    continue
                writer.writerow(labels)
                csvfile_out.flush()


if '__main__' == __name__:
    if not 3 == len(sys.argv):
        print ('usage: wikidata_org.py input_file.csv output_file.csv')
        sys.exit(1)
    fn_in = sys.argv[1]
    fn_out = sys.argv[2]
    main(fn_in, fn_out)

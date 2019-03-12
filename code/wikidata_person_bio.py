#!/usr/bin/python3

#
# Copyright (C) 2019 by Andrew Ziem.  All rights reserved.
# License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
# This is free software: you are free to change and redistribute it.
# There is NO WARRANTY, to the extent permitted by law.

"""
This program downloads basic biographical data about people using
SPARL queries to Wikidata.

The output files are untransformed CSV files. Each date of birth
is a separate file, so combine them with a script.

Tip: run a few in parallel, each with a separate time period. To be
nice to the servers, do not run too many processes at once.
"""

import datetime
import os
import sys

url = 'https://query.wikidata.org/sparql'

data_dir = "../data/wikidata/"

timeout_seconds = 120


def get_dob(dob):
    dob_str = dob.isoformat()
    csv_fn = os.path.join(data_dir, dob_str+".csv")
    if os.path.exists(csv_fn):
        print("Skipping DOB %s because it exists" % dob)
        return
    print("Querying the date of birth: %s" % dob)
    query = """
    SELECT
        ?person
        ?personLabel
        ?family_nameLabel
        ?given_nameLabel
        ?sex_or_genderLabel
        ?dob
        ?country_of_citizenshipLabel
        ?ethnic_groupLabel
	WHERE
	{
	  ?person wdt:P31 wd:Q5;
		  wdt:P569 ?dob

	  optional { ?person wdt:P734 ?family_name. }
	  optional { ?person wdt:P735 ?given_name. }
	  OPTIONAL { ?person wdt:P21 ?sex_or_gender. }
	  OPTIONAL { ?person wdt:P27 ?country_of_citizenship. }
	  OPTIONAL { ?person wdt:P172 ?ethnic_group. }
	  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
	  FILTER("%s"^^xsd:dateTime = ?dob).
	}
    """ % dob_str
    headers = {'Accept': 'text/csv'}
    import requests
    try:
        result_r = requests.get(
            url, params={'query': query}, headers=headers, timeout=timeout_seconds)
    except requests.exceptions.ReadTimeout:
        print('read timeout')
        import time
        time.sleep(10)
        return

    with open(csv_fn, 'wb') as f:
        f.write(result_r.text.encode('utf-8'))


def go():
    if not os.path.exists(data_dir):
        print('Making data directory: %s' % data_dir)
        os.mkdir(data_dir)
    if not len(sys.argv) == 3:
        print('As arguments pass the beginning and ending year of birth.')
        print('Example: python3 %s 1950 1960' % sys.argv[0])
        sys.exit(1)
    year_start = int(sys.argv[1])
    year_end = int(sys.argv[2])
    d = datetime.date(year_start, 1, 1)
    while d < datetime.date(year_end, 1, 1):
        get_dob(d)
        d += datetime.timedelta(days=1)


go()

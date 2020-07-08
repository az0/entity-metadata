#!/usr/bin/python3

#
# Copyright (C) 2019-2020 by Compassion International.  All rights reserved.
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
import time

url = 'https://query.wikidata.org/sparql'

data_dir = "../data/wikidata/"

timeout_seconds = 120


def get_dob(dob):
    dob_str = dob.isoformat()
    csv_fn = os.path.join(data_dir, dob_str+".csv")
    print(f'Querying the date of birth: {dob}')
    if os.path.exists(csv_fn):
        print(f' {dob}: Skipping because its file already exists.')
        return
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
        print(f' {dob}: network read timeout')
        time.sleep(10)
        return

    is_error = False
    server_error_msg = 'Our servers are currently under maintenance or experiencing a technical problem'
    if server_error_msg in result_r.text:
        print(f' {dob}: {server_error_msg}')
        is_error = True

    if len(result_r.text) == 0:
        print(f' {dob}: The server returned an empty file, so not saving it.')
        is_error = True

    hdr_row = 'person,personLabel,family_nameLabel,given_nameLabel,sex_or_genderLabel,dob,country_of_citizenshipLabel,ethnic_groupLabel'
    if result_r.text == hdr_row:
        print(f' {dob}: The server returned just a header, so not saving it')
        is_error = True

    if is_error:
        time.sleep(10)
        return

    with open(csv_fn, 'wb') as f:
        f.write(result_r.text.encode('utf-8'))


def go():
    if not os.path.exists(data_dir):
        print('Making data directory: %s' % data_dir)
        os.mkdir(data_dir)
    if not len(sys.argv) == 4:
        print('Argument 1: beginning year')
        print('Argument 2: ending year')
        print('Argument 3: concurrent processes')
        print('Loop starts on January 1 of beginning year and continues through December 31 of ending year.')
        print(f'Example: python3 {sys.argv[0]} 1950 1960 5')
        sys.exit(1)
    year_start = int(sys.argv[1])
    year_end = int(sys.argv[2])
    process_count = int(sys.argv[3])
    if process_count > 5:
        print('Warning: Wikidata has a limit of 5. See https://www.mediawiki.org/wiki/Wikidata_Query_Service/User_Manual#Query_limits')
    dates = []
    d = datetime.date(year_start, 1, 1)
    while d <= datetime.date(year_end, 12, 31):
        dates.append(d)
        d += datetime.timedelta(days=1)
    from multiprocessing import Pool, TimeoutError
    pool = Pool(processes=process_count)
    for i in pool.imap_unordered(get_dob, dates):
        pass

if __name__ == '__main__':
    go()

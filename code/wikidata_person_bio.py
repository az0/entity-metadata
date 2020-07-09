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


def get_dob(dob, data_dir, timeout_seconds, success_sleep, error_sleep):
    """Download a CSV file from Wikidata for a single date of birth"""
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
    import http
    import requests
    try:
        result_r = requests.get(
            url, params={'query': query}, headers=headers, timeout=timeout_seconds)
    except http.client.RemoteDisconnected:
        print(f' {dob}: Remote end closed connection without response')
        time.sleep(error_sleep)
        return
    except requests.exceptions.ReadTimeout:
        print(f' {dob}: network read timeout')
        time.sleep(error_sleep)
        return

    is_error = False

    if not result_r.status_code == 200:
        print(f' {dob}: HTTP status code {result_r.status_code}')
        is_error = True

    server_error_msg = 'Our servers are currently under maintenance or experiencing a technical problem'
    if server_error_msg in result_r.text:
        print(f' {dob}: {server_error_msg}')
        is_error = True

    if len(result_r.text) == 0:
        print(f' {dob}: The server returned an empty file, so not saving it.')
        is_error = True

    if is_error:
        # "One client (user agent + IP) is allowed 60 seconds of processing time each 60 seconds"
        # https://www.mediawiki.org/wiki/Wikidata_Query_Service/User_Manual#Query_limits
        time.sleep(error_sleep)
        return

    hdr_row = 'person,personLabel,family_nameLabel,given_nameLabel,sex_or_genderLabel,dob,country_of_citizenshipLabel,ethnic_groupLabel'
    if result_r.text.strip('\n').strip('\r') == hdr_row:
        print(
            f' {dob}: The server returned just a header, so there were zero results.')

    with open(csv_fn, 'wb') as f:
        f.write(result_r.text.encode('utf-8'))

    time.sleep(success_sleep)


def go():
    import argparse

    parser = argparse.ArgumentParser(
        description='Download personal biographies from Wikidata as CSV files')
    parser.add_argument(
        'beginning_year', help='begin downloading on January 1 of this year', type=int)
    parser.add_argument(
        'ending_year', help='end downloading on December 31 of this year', type=int)
    parser.add_argument(
        '-d', '--data-dir', help='destination directory for CSV files', default='data')
    parser.add_argument(
        '-p', '--parallel', help='number of parallel processes', default=1, type=int)
    parser.add_argument('-e', '--error-sleep',
                        help='number of seconds to sleep after an error', default=60, type=float)
    parser.add_argument('-s', '--success-sleep',
                        help='number of seconds to sleep after a success', default=0.5, type=float)
    parser.add_argument(
        '-t', '--timeout', help='number of seconds to wait for a response', default=120, type=int)
    args = parser.parse_args()

    if not os.path.exists(args.data_dir):
        print(f'Making data directory: {args.data_dir}')
        os.mkdir(args.data_dir)
    if args.parallel > 5:
        print('Warning: Wikidata has a limit of 5 parallel queries. See https://www.mediawiki.org/wiki/Wikidata_Query_Service/User_Manual#Query_limits')
    dates = []
    d = datetime.date(args.beginning_year, 1, 1)
    while d <= datetime.date(args.ending_year, 12, 31):
        dates.append(d)
        d += datetime.timedelta(days=1)
    kwargs = {'data_dir': args.data_dir,
              'timeout_seconds': args.timeout,
              'success_sleep':  args.success_sleep,
              'error_sleep':  args.error_sleep}

    if args.parallel > 1:
        # process in parallel
        from multiprocessing import Pool
        from functools import partial
        pool = Pool(processes=args.parallel)
        func = partial(get_dob, **kwargs)
        for i in pool.imap_unordered(func, dates):
            pass
    else:
        # process one at a time
        for date in dates:
            get_dob(date, **kwargs)


if __name__ == '__main__':
    go()

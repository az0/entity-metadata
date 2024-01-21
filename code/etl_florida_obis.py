#!/usr/bin/python3

#
# Copyright (C) 2024 by Compassion International.  All rights reserved.
# License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
# This is free software: you are free to change and redistribute it.
# There is NO WARRANTY, to the extent permitted by law.


"""
ETL the Florida OBIS database from multiple zip files into a single CSV

Keep only the ID, name, sex, and birth date

Get the data from here:
https://fdc.myflorida.com/pub/obis_request.html
"""

import pandas as pd
import zipfile
import os
import sys

WANT_COLS = ["DCNumber", "FirstName", "MiddleName", "LastName",
             "NameSuffix", "Race", "BirthDate", 'RecordType']


def groupby(df, column_name):
    """
    This function takes a pandas dataframe and a column name as input,
    and returns the top 20 frequencies of the values in that column.

    Args:
        df: A pandas dataframe.
        column_name: The name of the column to analyze.

    Returns:
        A pandas dataframe with the top 20 frequencies of the values in the specified column.
    """

    # Group the dataframe by the specified column and get the counts.
    value_counts = df[column_name].value_counts()

    # Sort the value counts in descending order and take the top 20.
    top_20_counts = value_counts.sort_values(ascending=False).head(20)

    # Reset the index to get a dataframe with columns 'Value' and 'Frequency'.
    top_20_counts = top_20_counts.reset_index(name='Frequency')

    # Rename the index column to 'Value'.
    top_20_counts.columns = ['Value', 'Frequency']
    print(top_20_counts)


def process_zip_files(directory):
    """
    Reads txt files from zip files in a directory, combines them into a single DataFrame,
    and exports the result to a CSV file.

    Args:
        directory (str): The path to the directory containing the zip files.
    """

    all_data = []
    for filename in os.listdir(directory):
        if filename.endswith(".zip"):
            print(f'processing zip {filename}')
            with zipfile.ZipFile(os.path.join(directory, filename), "r") as zip_ref:
                for zip_info in zip_ref.infolist():
                    if zip_info.filename.endswith(".txt"):
                        with zip_ref.open(zip_info.filename) as txt_file:
                            df = pd.read_csv(txt_file, sep="\t")
                            has_cols = df.columns
                            if not 'FirstName' in has_cols:
                                print(f'omitting {zip_info.filename}')
                                continue
                            print(f'keeping {zip_info.filename}')
                            fn_split = zip_info.filename.split('.')[
                                0].split('_')
                            record_type = zip_info.filename.split('.')[
                                0].lower()
                            keep_cols = list(set(WANT_COLS) & set(has_cols))
                            df = df[keep_cols]
                            df['RecordType'] = record_type
                            all_data.append(df)

    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df = combined_df[WANT_COLS]  # sort
    return combined_df


def go():
    if not len(sys.argv) == 3:
        print('As arguments pass (1) directory of Florida OBIS database as zip files and (2) the output .csv filename.')
        print('Example: python3 %s /foo/florida_obis/ florida_obis.csv' %
              sys.argv[0])
        sys.exit(1)
    directory = sys.argv[1]
    output_fn = sys.argv[2]
    df = process_zip_files(directory)
    groupby(df, 'RecordType')
    groupby(df, 'Race')
    groupby(df, 'NameSuffix')
    df.to_csv(output_fn, index=False)


go()

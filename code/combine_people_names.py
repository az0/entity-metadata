#!/usr/bin/python3

#
# Copyright (C) 2019 by Compassion International.  All rights reserved.
# License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
# This is free software: you are free to change and redistribute it.
# There is NO WARRANTY, to the extent permitted by law.


"""
This program generates names of people using a database and
rules. The names it creates follow patterns seen in the real
world lists but not in many public databases of individuals.

Examples of output:
Mr. John Smith VIII
Jane Smith PhD
John and Jane Smith
Smith Family
"""

import random
import pandas as pd
import numpy as np

styles_list = (
    '{given}',
    '{given} {surname}',
    '{prefix} {given} {surname}',
    '{given} {surname} {suffix}',
    '{male} {conjunction} {female}',
    '{female} {conjunction} {male}',
    '{male} {conjunction} {female} {surname}',
    '{male_prefix} {conjunction} {female_prefix} {male} {surname}',
    '{surname} Family',
    'The {surname} Family')
styles = {i: styles_list[i] for i in range(len(styles_list))}
style_count = len(styles)

# The multipliers are for a weighted random selection because some prefixes are
# more popular than others in the real world.
neutral_prefix = ['Dr.'] * 10 + ['Rev.', 'LTC', 'LtCol.', 'LCDR', 'SSgt']
male_prefix = ['Mr.'] * 20 + neutral_prefix
female_prefix = ['Miss', 'Ms.', 'Mrs.'] * 20 + neutral_prefix

# https://en.wikipedia.org/wiki/Post-nominal_letters
# https://en.wikipedia.org/wiki/List_of_professional_designations_in_the_United_States
neutral_suffix = ['PhD', 'CPA', 'MD', 'USN', 'USAF', 'USMC', 'USCG']
male_suffix = ['Sr.', 'Jr.', 'II', 'III', 'IV', 'V', 'VI', 'VII',
               'VIII', 'IX', 'X']
female_suffix = neutral_suffix

conjunction = ['and', '&'] * 10 + ['/']


def generate_name(row):
    """Generate a name given a row with basic name components"""
    name = styles[row['condition']].format(**row.to_dict())
    return name


def get_input(input_fn):
    """Read and prepare the input"""
    print('Reading file:', input_fn)
    wiki = pd.read_csv(input_fn)
    print('Original row count: {:,}'.format(wiki.shape[0]))
    print('Filtering')
    keep_cols = ['given_nameLabel', 'family_nameLabel', 'sex_or_genderLabel']
    keep_rows_g = wiki.sex_or_genderLabel.isin(('male', 'female'))
    keep_rows_c = wiki.country_of_citizenshipLabel.isin(
        ('United States of America', 'Canada', 'United Kingdom'))
    keep_rows = keep_rows_g & keep_rows_c
    wiki = wiki[keep_rows][keep_cols]
    wiki.dropna(inplace=True)
    new_cols = {'given_nameLabel': 'given',
                'family_nameLabel': 'surname', 'sex_or_genderLabel': 'gender'}
    wiki.rename(index=str, columns=new_cols, inplace=True)
    print('Filtered row count: {:,}'.format(wiki.shape[0]))
    return wiki


def generate_names(comb):
    def add_sample_col(choices, label):
        new_col = pd.DataFrame(choices, columns=[label]).sample(
            n=comb.shape[0], replace=True).reset_index(drop=True)
        return comb.join(new_col)
    comb = add_sample_col(male_prefix, 'male_prefix')
    comb = add_sample_col(female_prefix, 'female_prefix')
    comb = add_sample_col(male_suffix, 'male_suffix')
    comb = add_sample_col(female_suffix, 'female_suffix')
    comb = add_sample_col(conjunction, 'conjunction')

    def add_randint(max_int, label):
        return comb.join(pd.DataFrame(np.random.randint(0, max_int, size=(comb.shape[0], 1)), columns=[label]))
    comb = add_randint(2, 'is_first_male')
    comb = add_randint(2, 'remove_punctuation')
    comb = add_randint(style_count, 'condition')

    def assign_first_person(idx, prefix_col, given_col, suffix_col):
        comb.loc[idx, 'prefix'] = comb.loc[idx, prefix_col]
        comb.loc[idx, 'given'] = comb.loc[idx, given_col]
        comb.loc[idx, 'suffix'] = comb.loc[idx, suffix_col]
    assign_first_person(comb.is_first_male == 0,
                        'female_prefix', 'female', 'female_suffix')
    assign_first_person(comb.is_first_male == 1,
                        'male_prefix', 'male', 'male_suffix')
    idx_punct = comb.remove_punctuation == 1

    def remove_punct(col_name):
        comb.loc[idx_punct, col_name] = comb.loc[idx_punct,
                                                 col_name].str.replace('.', '')
    remove_punct('prefix')
    remove_punct('male_prefix')
    remove_punct('female_prefix')
    remove_punct('suffix')
    comb['name'] = comb.apply(generate_name, axis=1)
    return comb


def go(input_fn, output_fn, count):
    """The main program"""

    wiki = get_input(input_fn)

    def process_column(df, col_name):
        # Earlier I dropped duplicates, but that skewed the final list
        # towards unusual names.
        # remove Wikidata ids like Q12345
        idx = df.iloc[:,0].str.match(r'Q\d{2}')
        print('count removed with Wikidata id: ', sum(idx))
        df = df[~idx]  # remove columns
        # sample() shuffles the rows
        col_count = min(count, df.shape[0])
        df = df.sample(n=col_count)

        if col_name:
            df.rename(index=str, columns={'given': col_name}, inplace=True)
        df = df.reset_index(drop=True)
        return df
    female = process_column(wiki[wiki.gender == 'female'][['given']], 'female')
    male = process_column(wiki[wiki.gender == 'male'][['given']], 'male')
    surname = process_column(wiki[['surname']], None)

    comb = male.join((female, surname), how='inner')
    print('List counts: male {:,}; female {:,}; surname {:,}; combined {:,}'.format(
        male.shape[0], female.shape[0], surname.shape[0], comb.shape[0]))

    print('Generating names')
    import time
    start_time = time.time()
    comb = generate_names(comb)
    print(f'Elapsed time for generation phase: {time.time()-start_time:.2f}')
    comb[['name']].to_csv(output_fn, index=False)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input_filename', help='Wikidata .csv file as generated from this repository')
    parser.add_argument('count', help='number of records to export', type=int)
    parser.add_argument('output_filename',
                        help='.csv file generated by the program')
    args = parser.parse_args()

    go(args.input_filename, args.output_filename, args.count)

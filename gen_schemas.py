"""Assist the standardised schemas for the various datasets

This script just creates the starter csv files to fill out manually

This script collects the header names for each survey file to generates a
csv file with the headers/descriptions in the correct order,
to enable standardising column names by hand.

The 2015 survey provides this information in the README
"""

import csv
from os.path import join


basedir = 'data'
schemadir = 'schema'


def gen_schema(title, fin, first_row=True, second_row=True, schema_file=False):
    """
    helper to put together a schema. generates a csv file to be used for


    fin : (string) input csv filename
    first_row : (bool) use first row
    second_row : (bool) use second row
    schema : (string) incoporate separate csv with schema of input data
    """

    with open(fin, 'r') as f:
        col1 = csv.reader([next(f).strip()], delimiter=',', quotechar='"')
        col1 = list(col1)[0]
        col2 = csv.reader([next(f).strip()], delimiter=',', quotechar='"')
        col2 = list(col2)[0]
    if second_row and not first_row:
        col1 = col2
    if schema_file:
        result = {}
        with open(schema_file,'r') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            for line in reader:
                result[line[0]] = line[1]

    with open(join(schemadir, f'{title}.csv'), 'w', newline='') as csvfile:
        writer = csv.writer(
            csvfile,
            delimiter=',',
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL
        )
        header = ['column', 'originalcol']
        if schema_file:
            header += ['question']
        elif first_row and second_row:
            header += ['second_col']
        writer.writerow(header)
        for i, col in enumerate(col1):
            row = ["", col]
            if first_row and second_row:
                row += [col2[i]]
            elif schema_file:
                row += [result[col]]
            writer.writerow(row)


# column headers are the questions in the first row
# multiselect options are given in the second row
fin_2row = [
    [2011, "2011 Stack Overflow Survey Results.csv"],
    [2012, "2012 Stack Overflow Survey Results.csv"],
    [2013, "2013 Stack Overflow Survey Responses.csv"],
    [2014, "2014 Stack Overflow Survey Responses.csv"],
]

for year, f in fin_2row:
    f = join(basedir, f)
    gen_schema(year, f, second_row=True)


# 2nd row contains the column header names
fin_1row = [
    [2015, "2015 Stack Overflow Developer Survey Responses.csv"],
]

for year, f in fin_1row:
    f = join(basedir, f)
    gen_schema(year, f, first_row=False)


# schema provided separately for 2017 - 2020
fin_schema = [
    [2017, "developer_survey_2017"],
    [2018, "developer_survey_2018"],
    [2019, "developer_survey_2019"],
    [2020, "developer_survey_2020"],
]

for year, directory in fin_schema:
    gen_schema(
        year,
        join(basedir, directory, "survey_results_public.csv"),
        second_row=False,
        schema_file=join(basedir, directory, "survey_results_schema.csv"))

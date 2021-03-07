# %%

import pandas as pd
from os.path import join
import lzma
import pickle

survey_folder = join("sources", "surveys")
schema_folder = join("schemas")

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 120)


def xzsave(obj, filename):
    """ compressed pickle """
    with lzma.open(filename, "wb") as f:
        pickle.dump(obj, f)


def xzload(filename):
    """ compressed pickle """
    with lzma.open(filename, "rb") as f:
        return pickle.loads(f.read())


def load(year, csvfile, skiprows, manual_dummy):
    """
    load and standardise survey columns
    year : survey year
    csvfile : csv file
    skiprows : rows to skip
    """
    print(year)
    fin = join(survey_folder, csvfile)
    schema = join(schema_folder, f"{year}.csv")
    names = pd.read_csv(schema, header=None)[0]
    df = pd.read_csv(
        fin,
        skiprows=skiprows,
        engine='python',  # utf-8 errors with default engine
        names=names,
        header=None
    )
    df['survey_year'] = year
    return df


def prep_label_standardisation(dfs, cols, split=None):
    """
    prep dict for common labeling of a column across datasets
    """
    print('{')
    for col in cols:
        unique = []
        for df in dfs:
            if col in df.columns and df[col].dtype == object:
                unique.extend(list(pd.unique(df[col].dropna())))
        unique = sorted(list(set(unique)))
        if split:
            unique = [u.split(';') for u in unique]
            unique = [v.strip() for s in unique for v in s]
            unique = sorted(list(set(unique)))
        print(f'    "{col}": {{')
        for u in unique:
            print(f'        "{u}" : ,')
        print("    }")
    print('}')


def manual_dummy(df, cat_cols):
    """  dummy columns are already present, convert to bool """
    for col in cat_cols:
        c = df.columns.map(lambda x: x.startswith(col+'_'))
        if c.any():
            df.loc[:, c] = df.loc[:, c].fillna(0)
            df.loc[:, c] = df.loc[:, c].ne(0).mul(1)


def string_dummy(df, cat_cols):
    """ convert string lists separated by ";" to dummy_cols """
    for col in cat_cols:
        a = df.pop(col).str.get_dummies(';', )
        a = a.rename(columns=lambda x : f'{col}_{x.replace(" ", "")}')
        df = pd.concat([df, a])


# %%

surveys = [
    load(2011, "2011 Stack Overflow Survey Results.csv", 2, True),
    load(2012, "2012 Stack Overflow Survey Results.csv", 2, True),
    load(2013, "2013 Stack Overflow Survey Responses.csv", 2, True),
    load(2014, "2014 Stack Overflow Survey Responses.csv", 2, True),
    load(2015, "2015 Stack Overflow Developer Survey Responses.csv", 2, True),
    load(2016, "2016 Stack Overflow Survey Results/2016 Stack Overflow Survey Responses.csv", 1, True),
    load(2017, "developer_survey_2017/survey_results_public.csv", 1, False),
    load(2018, "developer_survey_2018/survey_results_public.csv", 1, False),
    load(2019, "developer_survey_2019/survey_results_public.csv", 1, False),
    load(2020, "developer_survey_2020/survey_results_public.csv", 1, False),
]

xzsave(surveys, "surveys.pz")

# %% reload

surveys = xzload("surveys.pz")

# %% columns of interest
# note that lang is made up of dummy columns for 2011-2015

interest_cols = [
    'salary',
    'satisfaction',
    'age',
    'gender',
    'years_coding',
    'dev_type',
    'employment',
    'industry',
    'org_size',
    'job_seek',
    'remote',
    'education',
    'undergrad',
    'os',
    'lang',
    # 'country',  # deal with country later
]

# %% lets see which years have which columns

ft = pd.DataFrame(columns=interest_cols, index=range(2011, 2021))
for s, y in zip(surveys, range(2011, 2021)):
    ft.loc[y] = ft.columns.map(lambda x: x in s.columns).astype(int)

print(ft.T)

#              2011 2012 2013 2014 2015 2016 2017 2018 2019 2020
# salary          1    1    1    1    1    1    1    1    1    1
# satisfaction    1    1    1    0    1    1    1    1    1    1
# age             1    1    1    1    1    1    0    1    1    1
# gender          0    0    0    1    1    1    1    1    1    1
# years_coding    1    1    1    1    1    1    1    1    1    1
# dev_type        1    1    1    1    1    1    1    1    1    1
# employment      0    0    0    0    1    1    1    1    1    1
# industry        1    1    1    1    1    1    1    0    0    0
# org_size        1    1    1    0    0    1    1    1    1    1
# job_seek        0    0    0    1    1    1    1    1    1    1
# remote          0    0    0    1    1    1    1    0    1    0
# education       0    0    0    0    0    1    1    1    1    1
# undergrad       0    0    0    0    0    0    1    1    1    1
# os              1    1    1    1    1    1    0    1    1    1
# lang            0    0    0    0    0    1    1    1    1    1

# %% manually map values between surveys where possible

prep_label_standardisation(surveys, interest_cols, split=';')


# %% 

split_2011 = [
    "lang",
]

split_2017 = [
    "dev_type",
    "education",
]

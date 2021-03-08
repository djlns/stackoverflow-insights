# %%

import pandas as pd
from os.path import join
import lzma
import pickle

survey_folder = join("sources", "surveys")
schema_folder = join("schemas")

pd.set_option('display.max_columns', None)


def xzsave(obj, filename):
    """ compressed pickle save """
    with lzma.open(filename, "wb") as f:
        pickle.dump(obj, f)


def xzload(filename):
    """ compressed pickle load """
    with lzma.open(filename, "rb") as f:
        return pickle.loads(f.read())


def load(year, csvfile, skiprows):
    """
    load and standardise survey columns, and add survey year column
    year : (int) survey year
    csvfile : (string) csv file
    skiprows : (int) rows to skip
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


def prep_label_standardisation(dfs, cols, split=";"):
    """
    prepare dict for manual common labeling across datasets
    dfs : (list of dataframes) surveys
    cols : (list of strings) columns of interest
    split : (string) split multicategory string entries
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
        print("    },")
    print('}')


# %%

surveys = [
    load(2011, "2011 Stack Overflow Survey Results.csv", 2),
    load(2012, "2012 Stack Overflow Survey Results.csv", 2),
    load(2013, "2013 Stack Overflow Survey Responses.csv", 2),
    load(2014, "2014 Stack Overflow Survey Responses.csv", 2),
    load(2015, "2015 Stack Overflow Developer Survey Responses.csv", 2),
    load(2016, "2016 Stack Overflow Survey Results/2016 Stack Overflow Survey Responses.csv", 1),
    load(2017, "developer_survey_2017/survey_results_public.csv", 1),
    load(2018, "developer_survey_2018/survey_results_public.csv", 1),
    load(2019, "developer_survey_2019/survey_results_public.csv", 1),
    load(2020, "developer_survey_2020/survey_results_public.csv", 1),
]

# %% columns of interest

interest_cols = [
    'salary',
    'satisfaction',
    'age',
    'gender',
    'years_coding',
    'occupation',
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
# occupation      1    1    1    1    1    1    1    1    1    1
# employment      0    0    0    0    1    1    1    1    1    1
# industry        1    1    1    1    1    1    1    0    0    0
# org_size        1    1    1    0    0    1    1    1    1    1
# job_seek        0    0    0    1    1    1    1    1    1    1
# remote          0    0    0    1    1    1    1    0    1    0
# education       0    0    0    0    0    1    1    1    1    1
# undergrad       0    0    0    0    0    0    1    1    1    1
# os              1    1    1    1    1    1    0    1    1    1
# lang            0    0    0    0    0    1    1    1    1    1

# %% develop a mapping dict to manually map values between surveys
# entries were conducted manually as the process requires domain knowledge
# and personal judgement

# prep_label_standardisation(surveys, interest_cols, split=';')


# %% the completed map dict has been stored in a separate file
from map_values import value_map


# %% standardise dummy variables - 2011 - 2015 csv files include dummy columns

split_2011 = [
    "lang",
]

split_2017 = [
    "dev_type",
    "education",
]

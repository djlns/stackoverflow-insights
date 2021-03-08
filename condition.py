# %%

import pandas as pd
from os.path import join
import lzma
import pickle
import seaborn as sns
import numpy as np

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

for df in surveys[:4]:
    for col in split_2011:
        c = df.columns.map(lambda x: x.startswith(col+'_'))
        df.loc[:, c] = df.loc[:, c].fillna(0)
        df.loc[:, c] = df.loc[:, c].ne(0).mul(1)

# %% - from 2016, certain columns became multicategorical
# stored as strings separated by ";"
# also standardise the column names in the process
# first split string into a list, then remap items and remove duplicates
# then return to a string so pandas can work it's magic for varibale length lists

split_2016 = [
    "occupation",
    "education",
    "lang",
]


def map_vals_list(x, col):
    try:
        return ';'.join(set([value_map[col][xi] for xi in x]))
    except TypeError:
        return x


for i, df in enumerate(surveys[4:]):
    print(pd.unique(df['survey_year']))
    new_cols = [df]
    for col in split_2016:
        if col in df:
            a = df.pop(col)
            a = a.str.split(r'\s*;\s*')
            a = a.map(lambda x: map_vals_list(x, col))
            a = a.str.get_dummies(';')
            a = a.rename(columns=lambda x : f'{col}_{x}')
            new_cols.append(a)
    surveys[i+4] = pd.concat(new_cols, axis=1)


# %% also from 2016, gender selection becomes more inclusive
# that makes it difficult to study, so
# lets split the dataset into female, male and other (if more than one is present)
# this stops double counting, keeps continutity between sets and
# avoiding more dummy variables

def map_gender(x):
    if x == np.nan:
        return
    try:
        return value_map["gender"][x]
    except KeyError:
        return "other"


for df in surveys[4:]:
    df["gender"] = df["gender"].map(map_gender)


# %% now, standardise data


def map_vals(x, col):
    try:
        return value_map[col][x]
    except KeyError:
        return x


for df in surveys:
    for col in interest_cols:
        if col in df.columns:
            df[col] = df[col].map(lambda x : map_vals(x, col))


# %% modify 2011-2015 datasets to match the dummy format of the later years

dummy_2016 = [
    "occupation",
    "education",
]

for i, df in enumerate(surveys[:4]):
    new_cols = [df]
    for col in dummy_2016:
        if col in df.columns:
            new_cols.append(pd.get_dummies(df.pop(col), prefix=col))
    surveys[i] = pd.concat(new_cols, axis=1)


# %% join them together

df = pd.concat(surveys)

# %% lets pick only the columns we want


def sel_cols(x):
    if x in ["survey_year"]+interest_cols:
        return True
    elif any(x.startswith(c+'_') for c in interest_cols):
        return True
    return False


df = pd.concat(surveys)
df = df.loc[:, df.columns.map(sel_cols)]


# %% lets try something

sns.catplot(x="survey_year",       # x variable name
            y="salary",       # y variable name
            hue="industry",  # group variable name
            data=df,     # dataframe to plot
            kind="bar",
            estimator=np.sum)


# %% finally, save the result

xzsave(df, "surveys.pz")

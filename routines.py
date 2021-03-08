import lzma
import pickle
from os.path import join
import pandas as pd

survey_folder = join("sources", "surveys")
schema_folder = join("schemas")


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
    print(year, end=' ')
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
    print(f"respondents: {df.shape[0]}, columns: {df.shape[1]}")
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

# %%

import pandas as pd
from os.path import join
import re

# pd.set_option('display.max_columns', None)
basepath = "surveys"


def gen_schema(fin, cols=None, second_row=True):
    """
    helper to put together a schema for a csv file where the questions
    are the column headers

    fin : (string) input csv file
    cols : (list) manual column titles for checking
    second_row : (bool) for csv files with a second row for categories
    """

    r = re.compile(
        r'''\s*([^,"']*?|"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')\s*(?:,|$)''',
        re.VERBOSE
    )
    with open(fin, 'r') as f:
        head1 = r.findall(next(f).strip())
        if second_row:
            head2 = r.findall(next(f).strip())
        else:
            head2 = False
    for i, h1 in enumerate(head1):
        if cols:
            print(f'{cols[i]:>25} :', end=' ')
        print(f'{h1[:50]:<50}', end=' ')
        if head2:
            print(f': {head2[i][:25]}', end='')
        print()


# %% 2011
# column headers are the questions
# multiselect options have their own columns
# options identified using the second header row

fin = join(basepath, "2011 Stack Overflow Survey Results.csv")

# create column names and mock up a schema

columns = [
    'country',
    'state',
    'age',
    'years_experience',
    'industry',
    'company_size',
    'occupation',
    'recommendation_likelihood',
    'purchaser_influencer',
    'purchaser_recommender',
    'purchaser_aprover',
    'purchaser_purchaser',
    'purchaser_checkwriter',
    'purchaser_none',
    'purchaser_seller',
    'purchasetype_hardware',
    'purchasetype_servers',
    'purchasetype_software',
    'purchasetype_pcs',
    'purchasetype_consultants',
    'purchasetype_other',
    'budget_0',
    'budget_10000',
    'budget_25000',
    'budget_40000',
    'budget_75000',
    'budget_100000',
    'budget_150000',
    'budget_unknown',
    'project_type',
    'lang_Java',
    'lang_JavaScript',
    'lang_CSS',
    'lang_PHP',
    'lang_Python',
    'lang_Ruby',
    'lang_SQL',
    'lang_C#',
    'lang_C++',
    'lang_C',
    'lang_Perl',
    'lang_none',
    'lang_other',
    'os',
    'satisfaction',
    'salary',
    'tech_iPhone',
    'tech_Android',
    'tech_Blackberry',
    'tech_OtherSmartPhone',
    'tech_RegularMobilePhone',
    'tech_Kindle',
    'tech_Nook',
    'tech_BluRay',
    'tech_HDTV',
    'tech_AppleTV',
    'tech_iPad',
    'tech_Netbook',
    'tech_PS3',
    'tech_Xbox',
    'tech_Wii',
    'tech_OtherGaming',
    'tech_Other',
    'spent_on_tech',
    'frequent_site',
]

gen_schema(fin, cols=columns)

# %%

# utf-8 errors by default, overcome using engine=python
df11 = pd.read_csv(
    fin,
    skiprows=2,
    engine='python',
    names=columns,
    header=None
)

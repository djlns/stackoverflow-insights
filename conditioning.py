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

# convert categorical columns to boolean
col_cat = [
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
]

df11[col_cat] = df11[col_cat].fillna(0)
df11[col_cat] = df11[col_cat].ne(0).mul(1)

df11

# %% columns of interest

cols_lang = [
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
    'lang_other'
]

cols = [
    'salary',
    'satisfaction',
    'country',
    'age',
    'years_experience',
    'company_size',
    'industry',
    'occupation',
    'project_type',
]

# for col in cols:
#    print(f"'{col}': {pd.unique(df11[col])},")

col_map = {
    "salary" : {
        "Student / Unemployed" : 0,
        "<$20,000" : 10000,
        "$20,000 - $40,000" : 30000,
        "$40,000 - $60,000" : 50000,
        "$60,000 - $80,000" : 70000,
        "$80,000 - $100,000" : 900000,
        "$100,000 - $120,000" : 110000,
        "$120,000 - $140,000" : 130000,
        ">$140,000" : 140000,
    },
    "satisfaction": {
        "FML": 1,
        "I'm not happy in my job": 2,
        "It pays the bills": 3,
        "I enjoy going to work": 4,
        "So happy it hurts": 5,
    },
    # "country": {
    #     "Africa",
    #     "Other Europe",
    #     "India",
    #     "Germany",
    #     "Other Asia",
    #     "Australia",
    #     "United States of America",
    #     "United Kingdom",
    #     "France",
    #     "Australasia",
    #     "Canada",
    #     "Russia",
    #     "South America",
    #     "Middle East",
    #     "Netherlands",
    #     "Italy",
    #     "North America (Other)",
    #     "Mexico",
    #     "Central America"
    # },
    "age": {
        "< 20" : 18,
        "20-24" : 22,
        "25-29" : 27,
        "30-34" : 32,
        "35-39" : 37,
        "40-50" : 45,
        "51-60" : 55,
        ">60" : 60,
    },
    "years_experience": {
        "<2" : 2,
        "41310" : 5,
        "41435" : 7,
        "11" : 11,
    },
    "company_size": {
        "Student" : 0,
        "Start Up (1-25)" : 25,
        "Mature Small Business (25-100)" : 100,
        "Mid Sized (100-999)" : 500,
        "Fortune 1000 (1,000+)" : 1000,
        "Other (not working, consultant, etc.)" : 1,
    },
    "industry": {
        "Software Products" : "Software",
        "Foundation / Non-Profit" : "NonProfit",
        "Web Services" : "Web",
        "Finance / Banking" : "Finance",
        # "Consulting",
        # "Manufacturing",
        # "Education",
        # "Other",
        # "Retail",
        # "Healthcare",
        # "Gaming",
        # "Advertising",
    },
    "occupation": {
        "Web Application Developer" : "Web",
        "Server Programmer" : "Server",
        "Executive (VP of Eng, CTO, CIO, etc.)" : "Executive",
        "Desktop Application Developer" : "Desktop",
        "IT Staff / System Administrator" : "System",
        "Database Administrator" : "Databse",
        "Manager of Developers or Team Leader" : "Manager",
        "Embedded Application Developer" : "Embedded",
        "Kernel / Driver Developer" : "Kernel",
        "Systems Analyst" : "SystemAnalyst",
        "IT Manager" : "IT",
        # "Student",
        # "Other",
    },
    # "project_type": {
    #     "Mobile",
    #     "Enterprise",
    #     "SaaS",
    #     "Other",
    #     "Web Platform",
    # }
}

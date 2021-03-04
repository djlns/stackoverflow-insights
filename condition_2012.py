# %%

import pandas as pd
import numpy as np
from os.path import join
import csv

pd.set_option('display.max_columns', None)
basepath = "surveys"


def gen_schema(fin, cols=None, second_row=True):
    """
    helper to put together a schema for a csv file where the questions
    are the column headers

    fin : (string) input csv file
    cols : (list) manual column titles for checking
    second_row : (bool) for csv files with a second row for categories
    """

    with open(fin, 'r') as f:
        head1 = csv.reader([next(f).strip()], delimiter=',', quotechar='"')
        head1 = list(head1)[0]
        if second_row:
            head2 = csv.reader([next(f).strip()], delimiter=',', quotechar='"')
            head2 = list(head2)[0]
        else:
            head2 = False
    if cols:
        print(f"len cols: {len(cols)}, len header: {len(head1)}")
        if len(cols) != len(head1):
            cols = None
    for i, h1 in enumerate(head1):
        if cols:
            print(f'{cols[i]:>25} :', end=' ')
        print(f'{h1[:50]:<60}', end=' ')
        if head2:
            print(f': {head2[i][:30]}', end='')
        print()


# %% 2012

fin = join(basepath, "2012 Stack Overflow Survey Results.csv")

columns = [
    'country',
    'state',
    'age',
    'years_experience',
    'industry',
    'company_size',
    'occupation',
    'purchaser_influencer',
    'purchaser_recommender',
    'purchaser_approver',
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
    'budget',
    'project_type',
    'lang_Java',
    'lang_JavaScript',
    'lang_CSS',
    'lang_PHP',
    'lang_Python',
    'lang_ObjectiveC',
    'lang_Ruby',
    'lang_SQL',
    'lang_C#',
    'lang_C++',
    'lang_C',
    'lang_Perl',
    'lang_HTML5',
    'lang_None',
    'lang_Other',
    'os',
    'satisfaction',
    'salary',
    'so_awareness',
    'so_profile',
    'so_profile_none_why',
    'so_profile_none_other',
    'tech_iPhone',
    'tech_Android',
    'tech_Blackberry',
    'tech_WindowsPhone',
    'tech_OtherSmartPhone',
    'tech_RegularMobilePhone',
    'tech_Kindle',
    'tech_Nook',
    'tech_AppleTV',
    'tech_Boxee',
    'tech_OtherStreaming',
    'tech_Netbook',
    'tech_PS3',
    'tech_Xbox',
    'tech_Wii',
    'tech_OtherGaming',
    'tech_KindleFire',
    'tech_iPad',
    'tech_Tablet',
    'tech_Other',
    'spent_on_tech',
    'so_ads_relevant',
    'so_ads_entertaining',
    'so_ads_informative',
    'so_ads_clicks',
    'so_ads_trial',
    'so_ads_blocker',
    'so_which_ads',
    'so_reputation',
    'so_frequent_site',
    'so_frequent_site_other',
]

gen_schema(fin, columns)

df12 = pd.read_csv(
    fin,
    skiprows=2,
    engine='python',
    names=columns,
    header=None
)

# %%

col_cat = [
    'purchaser_influencer',
    'purchaser_recommender',
    'purchaser_approver',
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
    'tech_iPhone',
    'tech_Android',
    'tech_Blackberry',
    'tech_WindowsPhone',
    'tech_OtherSmartPhone',
    'tech_RegularMobilePhone',
    'tech_Kindle',
    'tech_Nook',
    'tech_AppleTV',
    'tech_Boxee',
    'tech_OtherStreaming',
    'tech_Netbook',
    'tech_PS3',
    'tech_Xbox',
    'tech_Wii',
    'tech_OtherGaming',
    'tech_KindleFire',
    'tech_iPad',
    'tech_Tablet',
    'tech_Other',
    'so_ads_relevant',
    'so_ads_entertaining',
    'so_ads_informative',
    'so_ads_clicks',
    'so_ads_trial',
    'so_ads_blocker',
    'lang_Java',
    'lang_JavaScript',
    'lang_CSS',
    'lang_PHP',
    'lang_Python',
    'lang_ObjectiveC',
    'lang_Ruby',
    'lang_SQL',
    'lang_C#',
    'lang_C++',
    'lang_C',
    'lang_Perl',
    'lang_HTML5',
    'lang_None',
    'lang_Other',
]

df12[col_cat] = df12[col_cat].fillna(0)
df12[col_cat] = df12[col_cat].ne(0).mul(1)

df12


# %%

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

for col in cols:
    print(f"'{col}': {pd.unique(df12[col])},")

# %%

col_map = {
    'salary': {
        'Rather not say' : np.nan,
        'Student / Unemployed' : 0,
        '<$20,000' : 10000,
        '$20,000 - $40,000' : 30000,
        '$40,000 - $60,000' : 50000,
        '$60,000 - $80,000' : 70000,
        '$80,000 - $100,000' : 90000,
        '$100,000 - $120,000' : 11000,
        '$120,000 - $140,000' : 130000,
        '>$140,000' : 140000,
    },
    'satisfaction': {
        'I wish I had a job!' : 0,
        'Hate my job' : 1,
        "I'm not happy in my job" : 2,
        'Its a paycheck' : 3,
        'I enjoy going to work' : 4,
        'Love my job' : 5,
    },
    # 'country': {
    #     'India',
    #     'Germany',
    #     'United Kingdom',
    #     'France',
    #     'United States of America',
    #     'Other Europe',
    #     'Russia',
    #     'Canada',
    #     'Italy',
    #     'Australia',
    #     'Netherlands',
    #     'Middle East',
    #     'North America (Other)',
    #     'Other Asia',
    #     'Africa',
    #     'Australasia',
    #     'South America',
    #     'Mexico',
    #     'Central America',
    #     'Bangladesh'
    # },
    'age': {
        '< 20' : 18,
        '20-24' : 22,
        '25-29' : 27,
        '30-34' : 32,
        '35-39' : 37,
        '40-50' : 45,
        '51-60' : 55,
        '>60' : 60,
    },
    'years_experience': {
        '<2' : 2,
        '40944' : 5,
        '41070' : 7,
        '11' : 11,
    },
    'company_size': {
        'Student' : 0,
        'Other (not working, consultant, etc.)' : 1,
        'Start Up (1-25)' : 25,
        'Mature Small Business (25-100)' : 100,
        'Mid Sized (100-999)' : 500,
        'Fortune 1000 (1,000+)' : 1000,
    },
    'industry': {
        'Software Products' : "Software",
        'Foundation / Non-Profit' : "NonProfit",
        'Web Services' : "Web",
        'Finance / Banking' : "Finance",
        # 'Consulting',
        # 'Other',
        # 'Gaming',
        # 'Advertising',
        # 'Education',
        # 'Manufacturing',
        # 'Retail',
        # 'Healthcare',
    },
    'occupation': {
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
        "I don't work in tech" : "NotTech",
        # 'Student',
        # "Other",
    },
    # 'project_type': {
    #     'SaaS',
    #     'Mobile',
    #     'Web Platform',
    #     'Enterprise',
    #     'Other',
    #     'None / Unemployed'
    # }
}

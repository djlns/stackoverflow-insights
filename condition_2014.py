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


# %% 2014

fin = join(basepath, "2014 Stack Overflow Survey Responses.csv")

columns = [
    'country',
    'country_other',
    'state',
    'age',
    'gender',
    'years_experience',
    'occupation',
    'salary',
    'industry',
    'developer_count',
    'remote',
    'remote_enjoyment',
    'remote_location',
    'mobileapp_iPhone',
    'mobileapp_iPad',
    'mobileapp_Android',
    'mobileapp_AndroidTablet',
    'mobileapp_WindowsPhone',
    'mobileapp_Other',
    'mobileapp_None',
    'timespent_NewFeatures',
    'timespent_Refactoring',
    'timespent_Bugs',
    'timespent_Support',
    'timespent_Meetings',
    'timespent_Learning',
    'timespent_Surfing',
    'timespent_NewJob',
    'timespent_StackExchange',
    'purchaser_recommender',
    'purchaser_influencer',
    'purchaser_purchaser',
    'purchaser_checkwriter',
    'purchaser_none',
    'purchasetype_hardware',
    'purchasetype_servers',
    'purchasetype_software',
    'purchasetype_pcs',
    'purchasetype_consultants',
    'purchasetype_recruitment',
    'purchasetype_other',
    'budget',
    'lang_C',
    'lang_C++',
    'lang_C#',
    'lang_Java',
    'lang_JavaScript',
    'lang_Node.js',
    'lang_ObjectiveC',
    'lang_PHP',
    'lang_Python',
    'lang_Ruby',
    'lang_SQL',
    'lang_Other',
    'interest_Node.js',
    'interest_Haskell',
    'interest_CoffeeScript',
    'interest_Dart',
    'interest_C++11',
    'interest_Redis',
    'interest_MongoDB',
    'interest_F#',
    'interest_Go',
    'interest_Hadoop',
    'interest_AngularJS',
    'interest_Cordova',
    'interest_ArduinoRpi',
    'os',
    'tech_iPhone',
    'tech_Android',
    'tech_WindowsPhone',
    'tech_iPad',
    'tech_AndroidTablet',
    'tech_KindleFire',
    'tech_WindowsTablet',
    'tech_PS3',
    'tech_PS4',
    'tech_Xbox360',
    'tech_XboxOne',
    'tech_Wii',
    'tech_WiiU',
    'tech_Other',
    'job_12months',
    'job_found',
    'job_found_other',
    'job_looking',
    'job_recruiter_contact',
    'jobcontact_Email',
    'jobcontact_LinkedIn',
    'jobcontact_Phone',
    'jobcontact_StackOverflow',
    'jobcontact_Twitter',
    'email_personalized',
    'email_mentionsMe',
    'email_salary',
    'email_team',
    'email_culture',
    'email_benefits',
    'email_SOlink',
    'jobboard_period',
    'so_awareness',
    'so_careers_profile',
    'so_ads_relevant',
    'so_ads_entertaining',
    'so_ads_informative',
    'so_ads_clicks',
    'so_ads_trial',
    'so_ads_indicate',
    'so_ads_blocker',
    'so_apptivate_awareness',
    'so_appativate_particpate',
    'so_reputation',
    'so_which_ads',
    'so_use_look',
    'so_use_ask',
    'so_use_answer',
    'so_use_job',
    'so_use_reputation',
    'so_use_other',
    'so_find_period',
]

gen_schema(fin, columns)

df14 = pd.read_csv(
    fin,
    skiprows=2,
    engine='python',
    names=columns,
    header=None
)

# %%

col_cat = [
    'mobileapp_iPhone',
    'mobileapp_iPad',
    'mobileapp_Android',
    'mobileapp_AndroidTablet',
    'mobileapp_WindowsPhone',
    'mobileapp_Other',
    'mobileapp_None',
    'timespent_NewFeatures',
    'timespent_Refactoring',
    'timespent_Bugs',
    'timespent_Support',
    'timespent_Meetings',
    'timespent_Learning',
    'timespent_Surfing',
    'timespent_NewJob',
    'timespent_StackExchange',
    'purchaser_recommender',
    'purchaser_influencer',
    'purchaser_purchaser',
    'purchaser_checkwriter',
    'purchaser_none',
    'purchasetype_hardware',
    'purchasetype_servers',
    'purchasetype_software',
    'purchasetype_pcs',
    'purchasetype_consultants',
    'purchasetype_recruitment',
    'purchasetype_other',
    'lang_C',
    'lang_C++',
    'lang_C#',
    'lang_Java',
    'lang_JavaScript',
    'lang_Node.js',
    'lang_ObjectiveC',
    'lang_PHP',
    'lang_Python',
    'lang_Ruby',
    'lang_SQL',
    'lang_Other',
    'interest_Node.js',
    'interest_Haskell',
    'interest_CoffeeScript',
    'interest_Dart',
    'interest_C++11',
    'interest_Redis',
    'interest_MongoDB',
    'interest_F#',
    'interest_Go',
    'interest_Hadoop',
    'interest_AngularJS',
    'interest_Cordova',
    'interest_ArduinoRpi',
    'tech_iPhone',
    'tech_Android',
    'tech_WindowsPhone',
    'tech_iPad',
    'tech_AndroidTablet',
    'tech_KindleFire',
    'tech_WindowsTablet',
    'tech_PS3',
    'tech_PS4',
    'tech_Xbox360',
    'tech_XboxOne',
    'tech_Wii',
    'tech_WiiU',
    'tech_Other',
    'jobcontact_Email',
    'jobcontact_LinkedIn',
    'jobcontact_Phone',
    'jobcontact_StackOverflow',
    'jobcontact_Twitter',
    'emailjob_personalized',
    'emailjob_mentionsMe',
    'emailjob_salary',
    'emailjob_team',
    'emailjob_culture',
    'emailjob_benefits',
    'emailjob_SOlink',
    'so_ads_relevant',
    'so_ads_entertaining',
    'so_ads_informative',
    'so_ads_clicks',
    'so_ads_trial',
    'so_ads_indicate',
    'so_ads_blocker',
    'so_use_look',
    'so_use_ask',
    'so_use_answer',
    'so_use_job',
    'so_use_reputation',
    'so_use_other',
]

df14[col_cat] = df14[col_cat].fillna(0)
df14[col_cat] = df14[col_cat].ne(0).mul(1)

df14

# %%

cols = [
    'salary',
    'country',
    'developer_count',
    'age',
    'years_experience',
    'industry',
    'occupation',
]

for col in cols:
    print(f"'{col}': {pd.unique(df14[col])},")

# %%

col_map = {
    'salary': {
        '$20,000 - $40,000' : 30000,
        'Student / Unemployed' : 0,
        '<$20,000' : 10000,
        'Rather not say' : np.nan,
        '$80,000 - $100,000' : 90000,
        '$60,000 - $80,000' : 70000,
        '$40,000 - $60,000' : 50000,
        '>$140,000' : 140000,
        '$100,000 - $120,000' : 110000,
        '$120,000 - $140,000' : 130000
    },
    # 'country': {
    #     'India',
    #     'Thailand',
    #     'Iran',
    #     'Ukraine',
    #     'Denmark',
    #     'United Kingdom'
    #     'New Zealand',
    #     'Israel',
    #     'Saudi Arabia',
    #     'Czech Republic',
    #     'United States'
    #     'Canada',
    #     'Germany',
    #     'Brazil',
    #     'Ireland',
    #     'Japan',
    #     'Finland',
    #     'Lithuania'
    #     'Italy',
    #     'Russia',
    #     'France',
    #     'Ecuador',
    #     'Spain',
    #     'Vietnam',
    #     'Chile',
    #     'China'
    #     'Netherlands',
    #     'Turkey',
    #     'Portugal',
    #     'Egypt',
    #     'Belgium',
    #     'Cambodia',
    #     'Mexico'
    #     'Puerto Rico',
    #     'Switzerland',
    #     'Croatia',
    #     'Romania',
    #     'Jordan',
    #     'Philippines'
    #     'Austria',
    #     'Bolivia',
    #     'Algeria',
    #     'Poland',
    #     'Tunisia',
    #     'Argentina',
    #     'Bulgaria'
    #     'Norway',
    #     'Malaysia',
    #     'Pakistan',
    #     'Australia',
    #     'Greece',
    #     'Sweden'
    #     'South Africa',
    #     'Slovakia',
    #     'Cyprus',
    #     'Moldova',
    #     'Morocco',
    #     'Palestine'
    #     'Luxembourg',
    #     'Hungary',
    #     'Bangladesh',
    #     'Dominican Republic',
    #     'Sri Lanka'
    #     'Armenia',
    #     'Belarus',
    #     'Kazakhstan',
    #     'Iceland',
    #     'Hong Kong',
    #     'Slovenia'
    #     'Venezuela',
    #     'Uruguay',
    #     'Other',
    #     'Latvia',
    #     'Serbia',
    #     'Estonia',
    #     'Singapore'
    #     'Nepal',
    #     'United Arab Emirates',
    #     'Costa Rica',
    #     'Colombia',
    #     'El Salvador'
    #     'Lebanon',
    #     'Bosnia and Herzegovina',
    #     'Taiwan',
    #     'Kuwait',
    #     'Peru'
    #     'Macedonia [FYROM]',
    #     'Myanmar [Burma]',
    #     'Indonesia',
    #     'South Korea',
    #     'Georgia'
    #     'Malta',
    #     'Kenya',
    #     'Nigeria',
    #     'Guatemala',
    #     'Ghana'
    # },
    'developer_count' : {
        '1/5/2014' : 1,
        '6/15/2014' : 5,
        '16-30' : 15,
        '31-50' : 30,
        '50-100' : 50,
        '100' : 100
    },
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
        '2/5/2014' : 5,
        '6/10/2014' : 7,
        '11' : 11
    },
    'industry': {
        'Finance / Banking' : 'Finance',
        'Not Currently Employed' : 'NotEmployed',
        'Software Products' : 'Software',
        'Web Services' : 'Web',
        'Foundation / Non-Profit' : 'NonProfit',
        # 'Healthcare',
        # 'Student'
        # 'Manufacturing',
        # 'Other'
        # 'Government',
        # 'Retail',
        # 'Consulting'
        # 'Advertising',
        # 'Education',
        # 'Gaming'
    },
    'occupation': {
        'Back-End Web Developer' : 'WebBackend',
        'Desktop Software Developer' : 'Desktop',
        'Full-Stack Web Developer' : 'Web',
        'Database Administrator' : 'Database',
        'IT Staff / System Administrator' : 'System',
        "I don't work in tech" : 'NotTech',
        'Enterprise Level Services' : 'Enterprise',
        'Front-End Web Developer' : 'WebFrontend',
        'Manager of Developers or Team Leader' : 'Manager',
        'Mobile Application Developer' : 'Mobile',
        'Embedded Application Developer' : 'Embeded',
        'Executive (VP of Eng, CTO, CIO, etc.)' : 'Executive',
        # 'Student',
        # 'Other',
        # 'DevOps',
    }
}


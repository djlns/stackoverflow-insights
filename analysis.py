# %%

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.metrics import r2_score
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from routines import xzload, mpl_defs, stackplot

mpl_defs()

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

target_cols = [
    'salary',
]

numerical_cols = [
    'age',
    'years_coding',
    'org_size',
]

categorical_cols = [
    'os',
    'satisfaction',
    'job_seek',
    'remote',
    'gender',
    'industry',
    'employment',
]

dummy_cols = [
    'occupation',
    'education',
]

other = [
    'survey_year',
    'countries',
]

df = xzload("surveys.pz")

for col in df.columns:
    if col.startswith("occupation_") or col.startswith("education_"):
        df[col].isna() == 0
        # df[col] = df[col].astype('category')


df.describe()

# %% age

fig, ax = plt.subplots()
g = sns.violinplot(data=df, x="survey_year", y="age", ax=ax)
ax.set_ylim(0,100)

age = df.groupby("survey_year")["age"].agg(["mean", "std"]).drop(2017)
fig, ax = plt.subplots()
ax.errorbar(age.index, age["mean"], age["std"])

age

# %% years coding

fig, ax = plt.subplots()
g = sns.violinplot(data=df, x="survey_year", y="years_coding", ax=ax)

yc = df.groupby("survey_year")["years_coding"].agg(["mean", "std"])
fig, ax = plt.subplots()
ax.errorbar(yc.index, yc["mean"], yc["std"])

yc

# %% org

years = [2011, 2012, 2013, 2016, 2017, 2018, 2019, 2020]
org = df.loc[df.survey_year.isin(years)]

plt.figure()
sns.violinplot(data=org, x="survey_year", y="org_size")
plt.figure()
sns.violinplot(data=org[org.org_size < 1000], x="survey_year", y="org_size")
plt.figure()
sns.violinplot(data=org[org.org_size < 200], x="survey_year", y="org_size")

org.groupby("survey_year")["org_size"].agg(["mean", "std"])

# %% operating system!

fig, ax = plt.subplots()
os = df.groupby('survey_year')['os'].value_counts(normalize=True).sort_index().unstack()
os.columns = ["MacOS", "Linux/BSD", "Windows"]
os.plot(ax=ax)
ax.set_title('Most used Operating System')
ax.set_xticks(range(2011,2021))
ax.margins(0,0)

# %% satisfaction

sat = df.groupby("survey_year")["satisfaction"].value_counts(normalize=True).sort_index().unstack()
sat.columns = ['Very Negative', 'Negative', 'Neutral', 'Positive', 'Very Positive']
ax = stackplot(sat.drop([2017, 2018]), "Satisfaction")


# %% look for jobs

fig, ax = plt.subplots()
js = df.groupby("survey_year")["job_seek"].value_counts(normalize=True).sort_index().unstack()
js.columns = ["Actively looking", "Not looking", "Open to new opportunities"]
js.drop(2014).plot(ax=ax)
ax.set_title('Looking for a new job?')
ax.set_xticks(range(2011,2021))
ax.margins(0, 0.05)
# %% employment status

emp = df.groupby("survey_year")["employment"].value_counts(normalize=True).sort_index().unstack()
emp = emp[["not-employed", "independent", "part-time", "full-time"]]
emp.columns = [
    "Not employed (student/retired/unemployed)",
    "Independent (contractor/self-employed)",
    "Part time position",
    "Full time position"
]
ax = stackplot(emp, "Employment Status")

# %% remote working

rem = df.groupby("survey_year")["remote"].value_counts(normalize=True).sort_index().unstack()
rem = rem[["never",  "occasional", "part_time", "full_time"]]
rem.columns = ["Never", "Occasionaly", "Part time", "All the time"]
ax = stackplot(rem, 'Remote Working')
ax.legend(loc=4, frameon=True)


# %% gender

gen = df.groupby("survey_year")["gender"].value_counts().sort_index().unstack()
gen.columns = ["Female", "Male", "Other\nNon-binary\nTransgender\nGenderqueer\nGender non-conforming"]
ax = stackplot(gen, "Gender")
ax.legend(loc=2)
ax.set_ylabel('Participants')

gen = df.groupby("survey_year")["gender"].value_counts(normalize=True).sort_index().unstack()
np.round(gen.T*100, 1)

# %% industry

ind = df.groupby("survey_year")["industry"].value_counts(normalize=True).sort_index().unstack()

ind = ind[[
    "consulting",
    "education",
    "finance",
    "gaming",
    "healthcare",
    "manufacturing",
    "non-profit",
    "retail",
    "software",
    "web"
]].drop(2017)

ax = stackplot(ind, "Select Industries", cmap="icefire_r")
ax.legend(loc=2, fontsize='small', ncol=4)

np.round(ind.T*100, 1)
ind.T.plot(kind="bar", cmap="icefire_r")

np.round(ind.T*100, 1)

# %% occupations

occ_cols = [c for c in df.columns if c.startswith("occupation")]

occ = df[["survey_year"]+occ_cols].groupby("survey_year").sum()
occ.columns = [c.split("_", 1)[-1] for c in occ_cols]

occ_interest = [
    # 'student',  # ignore students
    'other',
    'non-tech',
    'academic',
    'data_engineer',
    'data_scientist',
    'analyst',
    'database',
    'DevOps',
    'executive',
    'manager',
    'admin',
    'QA',
    # 'sales',  very small contribution
    'designer',
    'dev_desktop',
    'dev_embed',
    'dev_enterprise',
    'dev_graphics',
    # 'dev_kernel',  # only included in early surveys
    'dev_mobile',
    'dev_server',
    'dev_stats',
    'dev_web-back',
    'dev_web-front',
    'dev_web-full',
    'dev_web',
]

occ = occ[occ_interest]

fig, ax = plt.subplots(figsize=(5,3))
ax = stackplot(occ, "occupations", cmap="Spectral", ax=ax)
ax.legend(bbox_to_anchor=(1,1), loc="upper left", ncol=2)

occ = occ.divide(occ.sum(axis=1).values, axis=0)
occ.columns = [c.split("_", 1)[-1] for c in occ_interest]

fig, ax = plt.subplots(figsize=(5,3))
ax = stackplot(occ.drop([2015,2017]), "occupations", cmap="tab20c", ax=ax)
ax.legend(bbox_to_anchor=(1,1), loc="upper left", ncol=2)

# %% focus on particular fields

occ_cols = [c for c in df.columns if c.startswith("occupation")]
occ = df[["survey_year"]+occ_cols].replace(np.nan, 0).groupby("survey_year").mean()

occ.columns = [c.split("_", 1)[-1] for c in occ_cols]
occ = occ[[
    'data_engineer',
    'data_scientist',
    'academic',
    'database',
    'analyst',
    'other',
]]

ax = stackplot(occ, "occupations")
ax.legend(loc=2, ncol=2)

fig, ax = plt.subplots()
for o in occ:
    l, = ax.plot(occ.index, occ[o], lw=1, label=o)
    if o == 'other':
        l.set_dashes((2, 2))
ax.legend(loc=2)
ax.margins(0,0.05)

np.round(occ*100, 2)

# %% see what sort of participants selected data_scientist

occ_cols = [c for c in df.columns if c.startswith("occupation")]
occ = df[["survey_year"]+occ_cols].loc[df.occupation_data_scientist == 1]
occ = occ.groupby("survey_year").mean()

occ.columns = [c.split("_", 1)[-1] for c in occ_cols]
occ = occ.dropna(axis=1, how='all').sort_values(by=2020, axis=1, ascending=False)
np.round(occ.drop([2015,2016]).T, 3) * 100


# %%  education

edu_cols = [c for c in df.columns if c.startswith("education")]
edu = df[["survey_year"]+edu_cols].groupby("survey_year").sum()
edu.columns = [c.split("_", 1)[-1] for c in edu_cols]

edu_formal = [
    'elementary',
    'secondary',
    'college',
    'bachelors',
    'masters',
    'doctoral',
    'associate_degree',
    'professional_degree',
]


eduf = edu[edu_formal]
dropcols = [2011, 2012, 2013, 2014]
eduf = eduf.divide(eduf.sum(axis=1).values, axis=0)
eduf = eduf.drop(dropcols).sort_values(by=2019,axis=1, ascending=False)
ax = stackplot(eduf, "formal education", cmap="vlag")
ax.legend(loc=3, ncol=2)

edu_informal = [
    'bootcamp',
    'competition',
    'hackathon',
    'mentor',
    'industry_cert',
    'night_school',
    'no_formal',
    'on_the_job',
    'online',
    'open_source',
    'self_taught'
]

edui = edu[edu_informal]
dropcols = [2011, 2012, 2013, 2014, 2020]
edui = edui.divide(edui.sum(axis=1).values, axis=0)
edui = edui.drop(dropcols).sort_values(by=2019,axis=1, ascending=False)
ax = stackplot(edui, "informal education", cmap="vlag")
ax.legend(loc=4, ncol=3)

# %% closer look

edu_interest_1 = [
    'bachelors',
    'masters',
    'doctoral',
]

edu_interest_2 = [
    'bootcamp',
    'online',
    'open_source',
    'on_the_job',
    'competition',
    'night_school'
]

edu_cols = [c for c in df.columns if c.startswith("education")]
edu = df[["survey_year"]+edu_cols].replace(np.nan, 0).groupby("survey_year").mean()
edu.columns = [c.split("_", 1)[-1] for c in edu_cols]

fig, ax = plt.subplots(1, 2, figsize=(5, 3))
edu[edu_interest_1].drop([2011, 2012, 2013, 2014]).plot(ax=ax[0])
edu[edu_interest_2].drop([2011, 2012, 2013, 2014, 2020]).plot(ax=ax[1])

for axi in ax:
    axi.margins(0, 0.05)

edu = edu[edu_interest_1+edu_interest_2].drop([2011, 2012, 2013, 2014])
np.round(edu * 100, 2).T

# %% Salary!

df.groupby('country').agg({'salary':'count'}).sort_values(by='salary', ascending=False).iloc[:10]

countries = [
    'United States',
    'United Kingdom',
    'India',
    'Germany',
    'Canada',
    'France',
    'Australia',
    'Russia',
    # 'Poland',
    # 'Brazil',
]

pd.pivot_table(
    df[df.country.isin(countries)],
    values='salary',
    columns=['survey_year'],
    index='country'
)

sns.violinplot(x='survey_year',y='salary',data=df.loc[df.country == "United States"])

# %%
Q = 0.95
ct = df.loc[df.country == "United States"].copy()
ct = ct[ct["salary"] < ct["salary"].quantile(Q)]

sns.violinplot(x='survey_year',y='salary',data=ct)

# %%

dfc = df[df.country.isin(countries)].copy()
dfc = dfc[dfc["salary"] < dfc["salary"].quantile(Q)]

pd.pivot_table(dfc, values='salary', columns=['survey_year'], index='country')

g = sns.catplot(
    x="country",
    y="salary",
    hue="survey_year",
    data=dfc,
    kind="bar",
    estimator=np.mean
)

# %% focus on US only

for year in range(2010,2021):

    dropcols = [
        'occupation_dev_server',
        'occupation_dev_kernel',
        'occupation_non-tech'
    ]

    Q = 0.95
    ct = df.loc[df.survey_year == year]
    ct = ct.loc[ct.country == "United States"].drop(dropcols, axis=1).copy()
    ct = ct[ct["salary"] < ct["salary"].quantile(Q)]

    covlist = ct.corr().unstack().drop_duplicates().sort_values()
    covlist = covlist[covlist < 1]  # remove self correlation

    covsort = []
    for (f1, f2), c in covlist.iteritems():
        if f1 == 'salary':
            covsort.append(f2)
        elif f2 == 'salary':
            covsort.append(f1)

    covmat = ct[['salary']+covsort[::-1]].corr()

    mask = np.triu(np.ones_like(covmat, dtype=bool))
    f, ax = plt.subplots(figsize=(11, 9))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    sns.heatmap(covmat, mask=mask, cmap=cmap, vmax=.3, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})

    covmat["salary"]

# %% final step, lets see how a simple model can fit the data


def clean_data(df):

    df = df.copy()
    df.dropna(subset=['salary'], inplace=True)
    df.dropna(how='all', axis=1, inplace=True)

    y = df['salary']
    df.drop('salary', axis=1, inplace=True)

    # separate numerical from categorical
    df_num = df.select_dtypes(include=np.number)
    df_cat = df.select_dtypes(include='object')

    # join numerical with nan filled with mean and one hot encoding for categorical
    X = pd.concat([
        df_num.apply(lambda col: col.fillna(col.mean())),
        pd.get_dummies(df_cat, dummy_na=False, drop_first=True)
    ], axis=1)

    return X, y


def run_regression(X, y, cutoff=0, alpha=0, test_size=.3, random_state=19):
    '''
    INPUT
    X - pandas dataframe, X matrix
    y - pandas dataframe, response variable
    cutoff - int, cutoff for number of non-zero values in dummy categorical vars
    alpha - float, L1-regularizer
    test_size - float between 0 and 1, default 0.3, determines the proportion of data as test data
    random_state - int, default 19, controls random state for train_test_split

    OUTPUT
    r2_scores_test - list of floats of r2 scores on the test data
    r2_scores_train - list of floats of r2 scores on the train data
    lm_model - model object from sklearn
    X_train, X_test, y_train, y_test - output from sklearn train test split used for optimal model
    '''

    reduce_X = X.iloc[:, (X.sum() > cutoff).values]

    X_train, X_test, y_train, y_test = train_test_split(
            reduce_X,
            y,
            test_size=test_size,
            random_state=random_state,
        )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    if alpha == 0:
        lm_model = LinearRegression()
    else:
        lm_model = Ridge(alpha=alpha)

    lm_model.fit(X_train, y_train)

    # Predict using your model
    y_test_preds = lm_model.predict(X_test)
    y_train_preds = lm_model.predict(X_train)

    # Score using your model
    test_score = r2_score(y_test, y_test_preds)
    train_score = r2_score(y_train, y_train_preds)

    print(reduce_X.shape)
    print(train_score, test_score)

    return test_score, train_score, lm_model, X_train, X_test, y_train, y_test


Q = 0.95
df2 = df[df["salary"] < df["salary"].quantile(Q)]
# df2 = df2.loc[df.country == "United States"].drop("country", axis=1)

X, y = clean_data(df2)
result = run_regression(X, y, alpha=0.01, cutoff=0)

# %%



# %%

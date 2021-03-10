# %%

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from routines import xzload, mpl_defs, stackplot

mpl_defs()

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

numerical_cols = [
    'salary',
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
    'undergrad',
    'countries',
    'survey_year',
]

df = xzload("surveys.pz")
df.describe()


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

# %%


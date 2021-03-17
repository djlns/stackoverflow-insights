# Stack Overflow Insights

## Project

### Motivation

The field of computing has developed incredibly rapidly over the past decade. How has this impacted the day to day life of developers, and how has the diversity of developers changed over this period? 

To investigate, this project uses the combined results from the [Stack Overflow](https://www.stackoverflow.com) Annual Developer survey, which has been conducted since 2011. It covers everything from favourite technologies to questions about careers, salaries and job preferences. In 2020 around 65,000 developers participated in the 20 minute survey, making it an unparalleled source of information regarding the field.

In particular I was interesting in the following questions:

1. What are the notable changes in demographics - e.g. in age, gender, education?
2. Do personal factors like satisfaction also show disernable trends?
3. How has the data science grown, and how has informal education like bootcamps and online courses evolved over this same period?
4. What of these factors have influenced salary?
5. Can we make a reasonable prediction of salary based upon these factors?


### Understanding the data

Each survey is contained in a separate .csv file. However, each year the types of question, the way they are asked, and even how they can be answered changes. As such, the first step was to study each survey and identify common questions. In the schemas folder, the questions from each year are listed in separate csv files. At the same time, the question names were standardised so they could be prepared and cominbined into a single dataset in the next step.


### Data preparation

The preparation of the data, which involves cleaning the data, transforming the different possible answers for question from each year to a common style, and necessary derivations are outlined in the [condition notebook](https://github.com/djlns/stackoverflow-insights/blob/main/condition.ipynb). The identified questions (columns) are as follows:

- salary: What is your annual compensation/salary in USD?
- country: What country do you live in?
- age: What is your age?
- gender: What is your gender?
- years_coding: How many years have you spent coding?
- occupation: How would you describe your occupation?
- industry: Which industry do you work in?
- satisfaction: How satisifed are you at work?
- job_seek: Are you currently looking for new opportunities?
- employment: What is your employment type (full-time/part-time)?
- org_size: What is your organisation size?
- remote: How often do you work remotely?
- education: What is your education level (formal and informal)
- os: Which operating system do you use / prefer?

The combined dataset was then saved into a single pandas pickled dataframe (surveys.pz).


### Analysis & Modelling

With this work complete, it was then possible to conduct an exploratory analysis of the entire dataset to address the project questions. This is presented in the [analysis notebook](https://github.com/djlns/stackoverflow-insights/blob/main/condition.ipynb)


### Evaluation

Modelling with salary as the target focused on a simple linear regression with L2-regularisation (ridge regressor) as a preliminary evaluation of whether or not a prediction of salary can be made based upon the other factors in the dataset. The resulting train/test R2-score of 0.63 / 0.63 is not amazing, indeed shows that it is possible in a promising first step. Further improvements could include more careful data conditioning with better approaches to imputing and the combination of the datasets, addressing multicollinearity between the predictors, and perhaps moving beyond a simple linear regression model.


### Findings

Some of the more interesting findings have been published in a [Medium post](https://djlns.medium.com/whats-changed-in-the-life-of-a-developer-since-2011-605107c54e5).


## Installation

Environment: Python 3.8+ with jupyter + pandas + seaborn + matplotlib + scikit-learn

Each year's survey is contained in a separate .csv file. These files can be accessed [here](https://insights.stackoverflow.com/survey) and should be unzipped as is into a folder named "sources" in the root of the project.


## License and Acknowledgements

You can find the Stack Overflow survey reports, datasets, and licensing information [here](https://insights.stackoverflow.com/survey). All credit to Stack Overflow for conducting the survey each year and freely providing the results. The work here is licensed under the MIT License, so feel free to copy and extend the code!

# Stack Overflow Insights

## Project Motivation

Since 2012 [Stack Overflow](https://www.stackoverflow.com) has conducted an Annual Developer survey that covers everything from favourite technologies to questions about careers, salaries and job preferences. In 2020 around 65,000 developers participated in the 20 minute survey, making it an unparalleled source of information regarding the field.

For this project I was interested in studying trends over time by comparing the surveys from 2011 to 2020. In particular I was interesting in the following questions:

1. What are the notable changes in demographics - e.g in age, gender, education?
2. Are there signs of occupation diversity in the field, and changes in personal factors like satisfaction?
3. How has the data science grown, and how has informal education like bootcamps and online courses evolved over this same period?
3. What are the primary factors correlated with salary in this comprehensive dataset?
4. Can we make a reasonable prediction of salary based upon the complete 2011-2020 dataset, using a simple linear regression model?

## Approach

Each survey is contained in a separate .csv file. The style of questions and possible answers changes each year. So, the first step was to identify interesting questions asked across multiple years, and then standardise the column names and responses. The combined dataset was then saved into a single pandas pickled dataframe (surveys.pz). The process is shown in the [condition notebook](https://github.com/djlns/stackoverflow-insights/blob/main/condition.ipynb) 

With this work complete, it was then possible to conduct an exploratory analysis of the entire dataset. This analysis is presented in the [analysis notebook](https://github.com/djlns/stackoverflow-insights/blob/main/condition.ipynb)

Some of the more interesting findings have been published in a [Medium post](https://djlns.medium.com/whats-changed-in-the-life-of-a-developer-since-2011-605107c54e5).

## Installation

Environment: Python 3.8+ with jupyter + pandas + seaborn + matplotlib + scikit-learn

Each year's survey is contained in a separate .csv file. These files can be accessed [here](https://insights.stackoverflow.com/survey) and should be unzipped as is into a folder named "sources" in the root of the project.

## License and Acknowledgements

You can find the Stack Overflow survey reports, datasets, and licensing information [here](https://insights.stackoverflow.com/survey). Credit to Stack Overflow for conducting the survey each year and freely providing the results. The work here licensed under the MIT License, so feel free to extend the code.

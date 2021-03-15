# Stack Overflow Insights

## Project Motivation

Since 2012 [Stack Overflow](https://www.stackoverflow.com) has conducted an Annual Developer survey that covers everything from favourite technologies to questions about careers, salaries and job preferences. In 2020 around 65,000 developers participated in the 20 minute survey, making it an unparalleled source of information regarding the field.

For this project I was interested in studying trends over time by comparing the surveys from 2011 to 2020. In particular I was interesting in the following questions:

1. What are the notable changes in demographics - e.g in age, gender, education
2. How about occupation diversity and personal factors like satisfaction.
3. More specifically, how has the use of informal education like bootcamps and online courses evolved over time.
3. What are the primary factors salaries also change?
4. Can we make a reasonable prediction of salary based upon the complete 2011-2020 dataset, using a simple linear regression model?


## Installation

Environment: Python 3.8+ with jupyter + pandas + matplotlib + scikit-learn

Each year's survey is contained in a separate .csv file. These files can be accessed [here](https://insights.stackoverflow.com/survey) and should be unzipped as is into a folder named "data" in the root of the project.

## Approach

First understand the data, in order to understand what sort of time information could gleaned, and the variables associated with those questions. Each year the survey format is slightly different. I first went about the process of extracting usable data from the csv files from 2011 to 2020, identifiying interesting questions from each year, while standardising the variable names. This made it possible at th end to combine the desired information into a single dataset with an additional column to identify the survey year.

I was also particularily interested in seeing any development in countries over the time. From 2014 onwards, the SO survey includes the [Big Mac index](https://github.com/TheEconomist/big-mac-data) and [UN sub-regions desigiations](https://unstats.un.org/unsd/methodology/m49/), which I extend to the earlier surveys in order to make a manageable look at how things change over time.

## License and Acknowledgements

You can find the Stack Overflow survey reports, datasets, and licensing information [here](https://insights.stackoverflow.com/survey).

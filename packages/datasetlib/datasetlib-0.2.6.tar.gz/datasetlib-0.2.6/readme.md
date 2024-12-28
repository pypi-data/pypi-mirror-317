# DataSetLib

## Introduction

a simple library having access to some often used datasets in pandas dataframe format

## Getting Started

There are two main functions in the module:

- `get_datasets()` returns a list with all the available datasets
- `get_dataset()` returns a specific dataset identified by a name

## Usage of datasetlib

```python
>>> import datasetlib as dsl
>>> dsl.get_datasets()
['aapl', 'amazon_reviews', 'avocado', 'babynames', 'bank_clients', 'bmw', 'canada_population', 
 'cancer', 'crypto_prices', 'crypto_returns', 'human_resources', 'project1_sales_data', 
 'project1_stores_data', 'sp500_prices', 'stock_prices', 'stocks', 'summergames', 
 'temperatures', 'titanic']
>>> dsl.get_dataset("titanic")
     survived  pclass     sex   age  sibsp  parch     fare embarked deck
0           0       3    male  22.0      1      0   7.2500        S  NaN
1           1       1  female  38.0      1      0  71.2833        C    C
2           1       3  female  26.0      0      0   7.9250        S  NaN
3           1       1  female  35.0      1      0  53.1000        S    C
4           0       3    male  35.0      0      0   8.0500        S  NaN
..        ...     ...     ...   ...    ...    ...      ...      ...  ...
886         0       2    male  27.0      0      0  13.0000        S  NaN
887         1       1  female  19.0      0      0  30.0000        S    B
888         0       3  female   NaN      1      2  23.4500        S  NaN
889         1       1    male  26.0      0      0  30.0000        C    C
890         0       3    male  32.0      0      0   7.7500        Q  NaN

[891 rows x 9 columns]
>>> 

```

## Project Homepage

<https://dev.azure.com/neuraldevelopment/datasetlib>

## Contribute

If you find a defect or suggest a new function, please send an eMail to <neutro2@outlook.de>

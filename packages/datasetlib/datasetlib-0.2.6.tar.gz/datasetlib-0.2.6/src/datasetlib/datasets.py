# =============================================================================
#
#  Licensed Materials, Property of Ralph Vogl, Munich
#
#  Project : basefunctions
#
#  Copyright (c) by Ralph Vogl
#
#  All rights reserved.
#
#  Description:
#
#  datasets provide basic access to well known datasets used for machine learning
#
# =============================================================================

# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------
import os
from typing import List

import basefunctions as bf
import pandas as pd

# -------------------------------------------------------------
# DEFINITIONS
# -------------------------------------------------------------

# -------------------------------------------------------------
# DEFINITIONS REGISTRY
# -------------------------------------------------------------

# -------------------------------------------------------------
# DEFINITIONS
# -------------------------------------------------------------
_dataset_dict = {
    "aapl": (
        "datasets/apple.csv",
        {"index_col": [0], "parse_dates": [0], "header": [0]},
    ),
    "amazon_reviews": (
        "datasets/amazon_reviews.csv",
        {"index_col": [0], "header": [0]},
    ),
    "avocado": ("datasets/avocado.csv", {"index_col": [0], "parse_dates": [0]}),
    "babynames": ("datasets/babynames.csv", {"index_col": [0]}),
    "bank_clients": ("datasets/bank_client_information.csv", {"header": [0]}),
    "bmw": ("datasets/bmw.csv", {"index_col": [0], "parse_dates": [0], "header": [0]}),
    "canada_population": ("datasets/canada_population.csv", {"header": [0]}),
    "cancer": ("datasets/cancer.csv", {"header": [0]}),
    "crypto_prices": (
        "datasets/crypto_daily_prices.csv",
        {"index_col": [0], "header": [0], "parse_dates": [0]},
    ),
    "crypto_returns": (
        "datasets/crypto_daily_returns.csv",
        {"index_col": [0], "header": [0], "parse_dates": [0]},
    ),
    "customer_complaints": (
        "datasets/customer_complaints.csv",
        {"index_col": [0], "parse_dates": [0], "header": [0]},
    ),
    # "ecommerce_sales": ("datasets/ecommerce_sales.csv", {"header": [0]}),
    "human_resources": ("datasets/human_resources.csv", {"header": [0]}),
    "project1_sales_data": ("datasets/project1_sales_data.csv", {"index_col": [0], "header": [0]}),
    "project1_stores_data": (
        "datasets/project1_stores_data.csv",
        {"index_col": [0], "header": [0]},
    ),
    "sp500_prices": ("datasets/sp500_prices.csv", {"header": [0]}),
    "stock_prices": (
        "datasets/stock_daily_prices.csv",
        {"index_col": [0], "parse_dates": [0], "header": [0]},
    ),
    "stocks": ("datasets/stocks.csv", {"index_col": [0], "parse_dates": [0], "header": [0, 1]}),
    "summergames": ("datasets/summergames.csv", {"index_col": [0], "header": [0]}),
    "temperatures": (
        "datasets/temperatures.csv",
        {"index_col": [0], "parse_dates": [0], "header": [0]},
    ),
    "titanic": ("datasets/titanic.csv", {}),
}


# -------------------------------------------------------------
# VARIABLE DEFINTIONS
# -------------------------------------------------------------


# -------------------------------------------------------------
# FUNCTION DEFINTIONS
# -------------------------------------------------------------
def get_datasets() -> List[str]:
    """get a list of all available datasets

    Returns
    -------
    list
        list of available datasets
    """
    return list(_dataset_dict.keys())


def get_dataset_filename(dataset_name: str) -> str | RuntimeError:
    """get the filename for a specific dataset

    Parameters
    ----------
    dataset_name : str
        name of dataset

    Returns
    -------
    str
        file name of dataset

    Raises
    ------
    RuntimeError
        raises RuntimeError if dataset name can't be found
    """
    if dataset_name in _dataset_dict:
        return bf.norm_path(
            os.path.sep.join(
                [
                    bf.get_path_name(os.path.abspath(__file__)),
                    _dataset_dict[dataset_name][0],
                ]
            )
        )
    else:
        raise RuntimeError(f"dataset {dataset_name} not found")


def get_dataset(dataset_name: str) -> pd.DataFrame | RuntimeError:
    """get a specific dataset

    Parameters
    ----------
    dataset_name : str
        name of dataset

    Returns
    -------
    pandas dataframe
        dataframe of dataset

    Raises
    ------
    RuntimeError
        raises RuntimeError if dataset name can't be found
    """
    if dataset_name in _dataset_dict:
        _, kwargs = _dataset_dict[dataset_name]
        return pd.read_csv(get_dataset_filename(dataset_name), **kwargs)
    else:
        raise RuntimeError(f"dataset {dataset_name} not found")

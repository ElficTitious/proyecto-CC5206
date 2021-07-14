import os as os
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import time

def encode_categorical_data(dataframe : pd.DataFrame) -> pd.DataFrame:
    """Method that given a pandas dataframe, returns a corresponding
    dataframe with each of its catecorical columns encoded using
    sklearn's LabelEncoder."""

    encoder = LabelEncoder()

    # For each column where the dtype is object, we encode using
    # LabelEncoder
    for column in dataframe.columns:
        if dataframe[column].dtype == "object":
            dataframe[column] = encoder.fit_transform(dataframe[column])

    return dataframe

def csv_to_df(year : int) -> pd.DataFrame:
    """Method that given a year in {2002, ..., 2020} reads the
    corresponding csv from datasets/cleansed and returns it as a
    dataframe."""
    this_path = os.path.dirname(os.path.realpath('__file__'))

    dataset_file_name = "rendimiento_{}.csv".format(year)

    path_file_dataset = os.path.join(this_path, "datasets/cleansed", dataset_file_name)
    dataframe = pd.read_csv(path_file_dataset, encoding = "ISO-8859-1")
    
    return dataframe

def split(dataframe : pd.DataFrame, test_size=0.3) -> tuple:
    """Method that given a rendimiento dataframe, splits the data
    into X_train, X_test, y_train and y_test."""
    X = dataframe.drop(columns="PROM_GRAL")
    y = dataframe["PROM_GRAL"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, stratify=y)

    return (X_train, X_test, y_train, y_test)


class TimerError(Exception):
    """Exception to report errors in Timer class"""


class Timer:

    def __init__(self):
        self._start_time = None


    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()


    def stop(self):
        """Method used for stoping the timer and returning the elapsed time
        since .start() was called.
        """
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        return elapsed_time
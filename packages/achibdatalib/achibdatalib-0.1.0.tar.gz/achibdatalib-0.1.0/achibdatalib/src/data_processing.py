# src/data_processing.py

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
import requests
from io import StringIO


class DataProcessor:
    """
    A class used to process data for analysis and modeling.

    Methods
    -------
    load_data(source)
        Loads data from a URL, file path, or DataFrame object.
    clean_data(df, strategy='drop')
        Cleans the DataFrame by handling missing values and duplicates.
    transform_data(df, columns, method='standard')
        Transforms the data using scaling methods.
    normalize_data(df, columns)
        Normalizes the data to have a mean of 0 and standard deviation of 1.
    bin_data(df, column, bins, labels)
        Bins data into discrete intervals.
    impute_missing_values(df, strategy='mean')
        Imputes missing values in the DataFrame.
    encode_categorical(df, columns)
        Encodes categorical columns using one-hot encoding.
    handle_outliers(df, columns, method='iqr')
        Handles outliers in the DataFrame.
    split_data(df, target_column, test_size=0.2)
        Splits the DataFrame into training and testing sets.
    aggregate_data(df, group_by_columns, agg_funcs)
        Aggregates data by specified columns and aggregation functions.
    merge_data(df1, df2, on, how='inner')
        Merges two DataFrames.
    pivot_data(df, index, columns, values)
        Pivots the DataFrame.
    filter_data(df, condition)
        Filters the DataFrame based on a condition.
    save_data(df, file_path)
        Saves the DataFrame to a specified file path.
    apply_function(df, func, axis=0)
        Applies a function along an axis of the DataFrame.
    map_values(df, column, mapping)
        Maps values in a column using a dictionary.
    """

    @staticmethod
    def load_data(source):
        """
        Load data from a URL, file path, or DataFrame object.

        Parameters
        ----------
        source : str or pandas.DataFrame
            The source of the data. Can be a URL, file path, or DataFrame object.

        Returns
        -------
        pandas.DataFrame
            The loaded DataFrame.
        """
        if isinstance(source, pd.DataFrame):
            return source
        elif source.startswith("http"):
            response = requests.get(source)
            data = StringIO(response.text)
            return pd.read_csv(data)
        else:
            return pd.read_csv(source)

    @staticmethod
    def clean_data(df, strategy="drop"):
        """
        Clean the DataFrame by handling missing values and duplicates.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame to clean.
        strategy : str, optional
            The strategy to use for cleaning ('drop', 'fill_mean', 'fill_median').

        Returns
        -------
        pandas.DataFrame
            The cleaned DataFrame.
        """
        if strategy == "drop":
            df = df.drop_duplicates()
            df = df.dropna()
        elif strategy == "fill_mean":
            df = df.fillna(df.mean())
        elif strategy == "fill_median":
            df = df.fillna(df.median())
        else:
            raise ValueError("Unsupported cleaning strategy")
        return df

    @staticmethod
    def transform_data(df, columns, method="standard"):
        """
        Transform the data using scaling methods.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame to transform.
        columns : list
            The columns to transform.
        method : str, optional
            The scaling method to use ('standard' or 'minmax').

        Returns
        -------
        pandas.DataFrame
            The transformed DataFrame.
        """
        if method == "standard":
            scaler = StandardScaler()
        elif method == "minmax":
            scaler = MinMaxScaler()
        else:
            raise ValueError("Unsupported transformation method")

        df[columns] = scaler.fit_transform(df[columns])
        return df

    @staticmethod
    def normalize_data(df, columns):
        """
        Normalize the data to have a mean of 0 and standard deviation of 1.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame to normalize.
        columns : list
            The columns to normalize.

        Returns
        -------
        pandas.DataFrame
            The normalized DataFrame.
        """
        scaler = StandardScaler()
        df[columns] = scaler.fit_transform(df[columns])
        return df

    @staticmethod
    def bin_data(df, column, bins, labels):
        """
        Bin data into discrete intervals.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the column to bin.
        column : str
            The column to bin.
        bins : list
            The bin edges.
        labels : list
            The labels for the bins.

        Returns
        -------
        pandas.DataFrame
            The DataFrame with binned data.
        """
        df[column] = pd.cut(df[column], bins=bins, labels=labels)
        return df

    @staticmethod
    def impute_missing_values(df, strategy="mean"):
        """
        Impute missing values in the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame with missing values.
        strategy : str, optional
            The strategy to use for imputation ('mean', 'median', 'mode').

        Returns
        -------
        pandas.DataFrame
            The DataFrame with imputed values.
        """
        if strategy == "mean":
            df = df.fillna(df.mean())
        elif strategy == "median":
            df = df.fillna(df.median())
        elif strategy == "mode":
            df = df.fillna(df.mode().iloc[0])
        else:
            raise ValueError("Unsupported imputation strategy")
        return df

    @staticmethod
    def encode_categorical(df, columns):
        """
        Encode categorical columns using one-hot encoding.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing categorical columns.
        columns : list
            The columns to encode.

        Returns
        -------
        pandas.DataFrame
            The DataFrame with encoded columns.
        """
        df = pd.get_dummies(df, columns=columns)
        return df

    @staticmethod
    def handle_outliers(df, columns, method="iqr"):
        """
        Handle outliers in the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing outliers.
        columns : list
            The columns to check for outliers.
        method : str, optional
            The method to use for handling outliers ('iqr' or 'zscore').

        Returns
        -------
        pandas.DataFrame
            The DataFrame with outliers handled.
        """
        if method == "iqr":
            for col in columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                df = df[(df[col] >= (Q1 - 1.5 * IQR)) & (df[col] <= (Q3 + 1.5 * IQR))]
        elif method == "zscore":
            for col in columns:
                df = df[(np.abs(df[col] - df[col].mean()) / df[col].std()) < 3]
        else:
            raise ValueError("Unsupported outlier handling method")

        return df

    @staticmethod
    def split_data(df, target_column, test_size=0.2):
        """
        Split the DataFrame into training and testing sets.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame to split.
        target_column : str
            The target column for prediction.
        test_size : float, optional
            The proportion of the dataset to include in the test split.

        Returns
        -------
        tuple
            The training and testing sets (X_train, X_test, y_train, y_test).
        """
        X = df.drop(columns=[target_column])
        y = df[target_column]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        return X_train, X_test, y_train, y_test

    @staticmethod
    def aggregate_data(df, group_by_columns, agg_funcs):
        """
        Aggregate data by specified columns and aggregation functions.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame to aggregate.
        group_by_columns : list
            The columns to group by.
        agg_funcs : dict
            The aggregation functions to apply.

        Returns
        -------
        pandas.DataFrame
            The aggregated DataFrame.
        """
        return df.groupby(group_by_columns).agg(agg_funcs)

    @staticmethod
    def merge_data(df1, df2, on, how="inner"):
        """
        Merge two DataFrames.

        Parameters
        ----------
        df1 : pandas.DataFrame
            The first DataFrame.
        df2 : pandas.DataFrame
            The second DataFrame.
        on : str
            The column to join on.
        how : str, optional
            The type of join to perform ('inner', 'outer', 'left', 'right').

        Returns
        -------
        pandas.DataFrame
            The merged DataFrame.
        """
        allowed_how = {
            "left": "left",
            "right": "right",
            "outer": "outer",
            "inner": "inner",
            "cross": "cross",
        }
        if how not in allowed_how:
            raise ValueError(
                f"Invalid value for 'how': {how}. Allowed values are {list(allowed_how.keys())}."
            )
        return pd.merge(df1, df2, on=on)

    @staticmethod
    def pivot_data(df, index, columns, values):
        """
        Pivot the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame to pivot.
        index : str
            The column to use as the new index.
        columns : str
            The column to use to make new columns.
        values : str
            The column to use for populating the new frame's values.

        Returns
        -------
        pandas.DataFrame
            The pivoted DataFrame.
        """
        return df.pivot(index=index, columns=columns, values=values)

    @staticmethod
    def filter_data(df, condition):
        """
        Filter the DataFrame based on a condition.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame to filter.
        condition : str
            The condition to filter by.

        Returns
        -------
        pandas.DataFrame
            The filtered DataFrame.
        """
        return df.query(condition)

    @staticmethod
    def save_data(df, file_path):
        """
        Save the DataFrame to a specified file path.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame to save.
        file_path : str
            The file path to save the DataFrame.

        Returns
        -------
        None
        """
        df.to_csv(file_path, index=False)

    @staticmethod
    def apply_function(df, func, axis=0):
        """
        Apply a function along an axis of the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame to apply the function to.
        func : function
            The function to apply.
        axis : int, optional
            The axis along which to apply the function (0 for rows, 1 for columns).

        Returns
        -------
        pandas.DataFrame
            The DataFrame with the function applied.
        """
        return df.apply(func, axis=axis)

    @staticmethod
    def map_values(df, column, mapping):
        """
        Map values in a column using a dictionary.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the column to map.
        column : str
            The column to map values in.
        mapping : dict
            The dictionary to map values.

        Returns
        -------
        pandas.DataFrame
            The DataFrame with mapped values.
        """
        df[column] = df[column].map(mapping)
        return df

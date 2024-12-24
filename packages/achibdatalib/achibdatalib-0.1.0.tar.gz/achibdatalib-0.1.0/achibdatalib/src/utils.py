import pandas as pd
import numpy as np


class Utils:
    """
    A class containing general utility functions for data operations.

    Methods
    -------
    calculate_mean(df, column)
        Calculates the mean of a specified column in the DataFrame.
    calculate_sum(df, column)
        Calculates the sum of a specified column in the DataFrame.
    calculate_max(df, column)
        Calculates the maximum value of a specified column in the DataFrame.
    calculate_min(df, column)
        Calculates the minimum value of a specified column in the DataFrame.
    calculate_std(df, column)
        Calculates the standard deviation of a specified column in the DataFrame.
    normalize_array(arr)
        Normalizes a numpy array.
    calculate_median(df, column)
        Calculates the median of a specified column in the DataFrame.
    calculate_variance(df, column)
        Calculates the variance of a specified column in the DataFrame.
    calculate_mode(df, column)
        Calculates the mode of a specified column in the DataFrame.
    calculate_iqr(df, column)
        Calculates the interquartile range (IQR) of a specified column in the DataFrame.
    """

    @staticmethod
    def calculate_mean(df, column):
        """
        Calculates the mean of a specified column in the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        column : str
            The column to calculate the mean for.

        Returns
        -------
        float
            The mean of the specified column.
        """
        return df[column].mean()

    @staticmethod
    def calculate_sum(df, column):
        """
        Calculates the sum of a specified column in the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        column : str
            The column to calculate the sum for.

        Returns
        -------
        float
            The sum of the specified column.
        """
        return df[column].sum()

    @staticmethod
    def calculate_max(df, column):
        """
        Calculates the maximum value of a specified column in the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        column : str
            The column to calculate the maximum value for.

        Returns
        -------
        float
            The maximum value of the specified column.
        """
        return df[column].max()

    @staticmethod
    def calculate_min(df, column):
        """
        Calculates the minimum value of a specified column in the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        column : str
            The column to calculate the minimum value for.

        Returns
        -------
        float
            The minimum value of the specified column.
        """
        return df[column].min()

    @staticmethod
    def calculate_std(df, column):
        """
        Calculates the standard deviation of a specified column in the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        column : str
            The column to calculate the standard deviation for.

        Returns
        -------
        float
            The standard deviation of the specified column.
        """
        return df[column].std()

    @staticmethod
    def normalize_array(arr):
        """
        Normalizes a numpy array.

        Parameters
        ----------
        arr : numpy.ndarray
            The array to normalize.

        Returns
        -------
        numpy.ndarray
            The normalized array.
        """
        return (arr - np.min(arr)) / (np.max(arr) - np.min(arr))

    @staticmethod
    def calculate_median(df, column):
        """
        Calculates the median of a specified column in the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        column : str
            The column to calculate the median for.

        Returns
        -------
        float
            The median of the specified column.
        """
        return df[column].median()

    @staticmethod
    def calculate_variance(df, column):
        """
        Calculates the variance of a specified column in the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        column : str
            The column to calculate the variance for.

        Returns
        -------
        float
            The variance of the specified column.
        """
        return df[column].var()

    @staticmethod
    def calculate_mode(df, column):
        """
        Calculates the mode of a specified column in the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        column : str
            The column to calculate the mode for.

        Returns
        -------
        float
            The mode of the specified column.
        """
        return df[column].mode()[0]

    @staticmethod
    def calculate_iqr(df, column):
        """
        Calculates the interquartile range (IQR) of a specified column in the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        column : str
            The column to calculate the IQR for.

        Returns
        -------
        float
            The IQR of the specified column.
        """
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        return Q3 - Q1

import pandas as pd
import numpy as np
from scipy import stats


class Statistics:
    """
    A class used to perform statistical analysis on data.

    Methods
    -------
    describe_data(df)
        Provides descriptive statistics for the DataFrame.
    correlation_matrix(df)
        Computes the correlation matrix for the DataFrame.
    t_test(sample1, sample2)
        Performs a t-test to compare the means of two samples.
    chi_square_test(observed, expected)
        Performs a chi-square test to compare observed and expected frequencies.
    anova(*samples)
        Performs a one-way ANOVA test to compare the means of multiple samples.
    linear_regression(x, y)
        Performs a linear regression analysis.
    z_score(df, column)
        Computes the z-scores for a column in the DataFrame.
    moving_average(df, column, window)
        Computes the moving average for a column in the DataFrame.
    """

    @staticmethod
    def describe_data(df):
        """
        Provides descriptive statistics for the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame to describe.

        Returns
        -------
        pandas.DataFrame
            The descriptive statistics of the DataFrame.
        """
        return df.describe()

    @staticmethod
    def correlation_matrix(df):
        """
        Computes the correlation matrix for the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame to compute the correlation matrix for.

        Returns
        -------
        pandas.DataFrame
            The correlation matrix of the DataFrame.
        """
        return df.corr()

    @staticmethod
    def t_test(sample1, sample2):
        """
        Performs a t-test to compare the means of two samples.

        Parameters
        ----------
        sample1 : array-like
            The first sample.
        sample2 : array-like
            The second sample.

        Returns
        -------
        tuple
            The t-statistic and the p-value.
        """
        return stats.ttest_ind(sample1, sample2)

    @staticmethod
    def chi_square_test(observed, expected):
        """
        Performs a chi-square test to compare observed and expected frequencies.

        Parameters
        ----------
        observed : array-like
            The observed frequencies.
        expected : array-like
            The expected frequencies.

        Returns
        -------
        tuple
            The chi-square statistic and the p-value.
        """
        return stats.chisquare(observed, expected)

    @staticmethod
    def anova(*samples):
        """
        Performs a one-way ANOVA test to compare the means of multiple samples.

        Parameters
        ----------
        samples : array-like
            The samples to compare.

        Returns
        -------
        tuple
            The F-statistic and the p-value.
        """
        return stats.f_oneway(*samples)

    @staticmethod
    def linear_regression(x, y):
        """
        Performs a linear regression analysis.

        Parameters
        ----------
        x : array-like
            The independent variable.
        y : array-like
            The dependent variable.

        Returns
        -------
        tuple
            The slope, intercept, r-value, p-value, and standard error of the estimate.
        """
        return stats.linregress(x, y)

    @staticmethod
    def z_score(df, column):
        """
        Computes the z-scores for a column in the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the column.
        column : str
            The column to compute z-scores for.

        Returns
        -------
        pandas.Series
            The z-scores of the column.
        """
        return (df[column] - df[column].mean()) / df[column].std()

    @staticmethod
    def moving_average(df, column, window):
        """
        Computes the moving average for a column in the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the column.
        column : str
            The column to compute the moving average for.
        window : int
            The window size for the moving average.

        Returns
        -------
        pandas.Series
            The moving average of the column.
        """
        return df[column].rolling(window=window).mean()

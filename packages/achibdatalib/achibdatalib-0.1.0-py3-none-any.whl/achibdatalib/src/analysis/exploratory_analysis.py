import pandas as pd
from src.data_processing import DataProcessor
from src.statistics import Statistics
from src.visualization import Visualizations


class ExploratoryAnalysis:
    """
    A class used to perform exploratory data analysis (EDA) on data.

    Methods
    -------
    load_and_clean_data(source, cleaning_strategy='drop')
        Loads and cleans the data from a specified source.
    describe_and_visualize_data(df)
        Provides descriptive statistics and visualizations for the DataFrame.
    analyze_correlations(df)
        Analyzes and visualizes correlations in the DataFrame.
    perform_statistical_tests(df, column1, column2)
        Performs statistical tests between two columns in the DataFrame.
    visualize_distributions(df, columns)
        Visualizes the distributions of specified columns in the DataFrame.
    """

    @staticmethod
    def load_and_clean_data(source, cleaning_strategy="drop"):
        """
        Loads and cleans the data from a specified source.

        Parameters
        ----------
        source : str or pandas.DataFrame
            The source of the data. Can be a URL, file path, or DataFrame object.
        cleaning_strategy : str, optional
            The strategy to use for cleaning ('drop', 'fill_mean', 'fill_median').

        Returns
        -------
        pandas.DataFrame
            The cleaned DataFrame.
        """
        df = DataProcessor.load_data(source)
        df = DataProcessor.clean_data(df, strategy=cleaning_strategy)
        return df

    @staticmethod
    def describe_and_visualize_data(df):
        """
        Provides descriptive statistics and visualizations for the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame to analyze.

        Returns
        -------
        None
        """
        # Descriptive statistics
        desc = Statistics.describe_data(df)
        print("Descriptive Statistics:\n", desc)

        # Visualizations
        for column in df.select_dtypes(include=["float64", "int64"]).columns:
            Visualizations.plot_histogram(df, column=column)
            Visualizations.plot_boxplot(df, column=column)

    @staticmethod
    def analyze_correlations(df):
        """
        Analyzes and visualizes correlations in the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame to analyze.

        Returns
        -------
        None
        """
        # Correlation matrix
        corr_matrix = Statistics.correlation_matrix(df)
        print("Correlation Matrix:\n", corr_matrix)

        # Heatmap
        Visualizations.plot_heatmap(df)

    @staticmethod
    def perform_statistical_tests(df, column1, column2):
        """
        Performs statistical tests between two columns in the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the columns.
        column1 : str
            The first column for the test.
        column2 : str
            The second column for the test.

        Returns
        -------
        None
        """
        # T-test
        t_stat, p_value = Statistics.t_test(df[column1].dropna(), df[column2].dropna())
        print(
            f"T-test between {column1} and {column2}: t-statistic = {t_stat}, p-value = {p_value}"
        )

        # Linear regression
        slope, intercept, r_value, p_value, std_err = Statistics.linear_regression(
            df[column1].dropna(), df[column2].dropna()
        )
        print(
            f"Linear Regression between {column1} and {column2}: slope = {slope}, intercept = {intercept}, r-value = {r_value}, p-value = {p_value}, std_err = {std_err}"
        )

    @staticmethod
    def visualize_distributions(df, columns):
        """
        Visualizes the distributions of specified columns in the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the columns.
        columns : list
            The columns to visualize.

        Returns
        -------
        None
        """
        for column in columns:
            Visualizations.plot_histogram(df, column=column)
            Visualizations.plot_violin(df, x=column, y=column)

# Import necessary modules and classes
from src.data_processing import DataProcessor
from src.statistics import Statistics
from src.visualization import Visualizations
from src.models.classification import Classification
from src.models.regression import Regression
from src.analysis.advanced_analysis import AdvancedAnalysis
from src.utils import Utils


# Main class to encapsulate the library's functionalities
class DataLib:
    """
    A class to encapsulate the main functionalities of the DataLib library.

    Methods
    -------
    load_and_clean_data(source, cleaning_strategy='drop')
        Loads and cleans the data from a specified source.
    describe_data(df)
        Provides descriptive statistics for the DataFrame.
    visualize_data(df, x_column, y_column=None)
        Provides visualizations for the DataFrame.
    perform_classification(df, target_column)
        Performs classification on the data.
    perform_regression(df, target_column)
        Performs regression on the data.
    perform_advanced_analysis(df, target_column)
        Performs advanced analysis on the data.
    analyze_data_engine(source, target_column, cleaning_strategy='drop')
        Executes a full analysis workflow for a given dataset.
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
            The descriptive statistics.
        """
        return Statistics.describe_data(df)

    @staticmethod
    def visualize_data(df, x_column, y_column=None):
        """
        Provides visualizations for the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame to visualize.
        x_column : str
            The column to visualize on the x-axis.
        y_column : str, optional
            The column to visualize on the y-axis for scatter plot (default is None).

        Returns
        -------
        None
        """
        Visualizations.plot_histogram(df, x_column)
        if y_column:
            Visualizations.plot_scatter(df, x_column, y_column)
        Visualizations.plot_boxplot(df, x_column)
        Visualizations.plot_heatmap(df)

    @staticmethod
    def perform_classification(df, target_column):
        """
        Performs classification on the data.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        target_column : str
            The target column for classification.

        Returns
        -------
        dict
            The results of the classification.
        """
        X_train, X_test, y_train, y_test = Classification.preprocess_data(
            df, target_column
        )
        return Classification.logistic_regression(X_train, y_train, X_test, y_test)

    @staticmethod
    def perform_regression(df, target_column):
        """
        Performs regression on the data.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        target_column : str
            The target column for regression.

        Returns
        -------
        dict
            The results of the regression.
        """
        X_train, X_test, y_train, y_test = Regression.preprocess_data(df, target_column)
        return Regression.linear_regression(X_train, y_train, X_test, y_test)

    @staticmethod
    def perform_advanced_analysis(df, target_column):
        """
        Performs advanced analysis on the data.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        target_column : str
            The target column for analysis.

        Returns
        -------
        dict
            The results of the advanced analysis.
        """
        return AdvancedAnalysis.perform_pca(df)

    @staticmethod
    def analyze_data_engine(source, target_column, cleaning_strategy="drop"):
        """
        Executes a full analysis workflow for a given dataset.

        Parameters
        ----------
        source : str or pandas.DataFrame
            The source of the data. Can be a URL, file path, or DataFrame object.
        target_column : str
            The target column for analysis.
        cleaning_strategy : str, optional
            The strategy to use for cleaning ('drop', 'fill_mean', 'fill_median').

        Returns
        -------
        dict
            The results of the full analysis including descriptive statistics, visualizations, and analysis results.
        """
        # Load and clean data
        df = DataLib.load_and_clean_data(source, cleaning_strategy)

        # Describe data
        description = DataLib.describe_data(df)

        # Visualize data
        DataLib.visualize_data(df, target_column)

        # Perform classification
        classification_results = DataLib.perform_classification(df, target_column)

        # Perform regression
        regression_results = DataLib.perform_regression(df, target_column)

        # Perform advanced analysis
        advanced_analysis_results = DataLib.perform_advanced_analysis(df, target_column)

        return {
            "description": description,
            "classification_results": classification_results,
            "regression_results": regression_results,
            "advanced_analysis_results": advanced_analysis_results,
        }

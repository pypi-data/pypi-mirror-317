import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from src.models.classification import Classification
from src.models.regression import Regression


class AdvancedAnalysis:
    """
    A class used to perform advanced analysis on data.

    Methods
    -------
    preprocess_data(df, target_column, test_size=0.2, scale_data=True)
        Preprocesses the data by splitting into training and testing sets and scaling if required.
    perform_pca(df, n_components=2)
        Performs Principal Component Analysis (PCA) on the data.
    perform_tsne(df, n_components=2, perplexity=30.0, n_iter=1000)
        Performs t-Distributed Stochastic Neighbor Embedding (t-SNE) on the data.
    logistic_regression(df, target_column)
        Performs logistic regression on the data.
    decision_tree(df, target_column)
        Performs decision tree classification on the data.
    random_forest(df, target_column)
        Performs random forest classification on the data.
    linear_regression(df, target_column)
        Performs linear regression on the data.
    ridge_regression(df, target_column, alpha=1.0)
        Performs ridge regression on the data.
    lasso_regression(df, target_column, alpha=1.0)
        Performs lasso regression on the data.
    decision_tree_regression(df, target_column)
        Performs decision tree regression on the data.
    random_forest_regression(df, target_column)
        Performs random forest regression on the data.
    """

    @staticmethod
    def preprocess_data(df, target_column, test_size=0.2, scale_data=True):
        """
        Preprocesses the data by splitting into training and testing sets and scaling if required.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        target_column : str
            The target column for analysis.
        test_size : float, optional
            The proportion of the dataset to include in the test split (default is 0.2).
        scale_data : bool, optional
            Whether to scale the data (default is True).

        Returns
        -------
        tuple
            The training and testing sets (X_train, X_test, y_train, y_test).
        """
        df = df.drop(columns=list(df.select_dtypes(include=["object"]).columns))
        X = df.drop(columns=[target_column])
        y = df[target_column]
        X_train, X_test, y_train, y_test = Classification.preprocess_data(
            df, target_column, test_size, scale_data
        )
        return X_train, X_test, y_train, y_test

    @staticmethod
    def perform_pca(df, n_components=2):
        """
        Performs Principal Component Analysis (PCA) on the data.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        n_components : int, optional
            The number of components to keep (default is 2).

        Returns
        -------
        pandas.DataFrame
            The DataFrame with the principal components.
        """
        df = df.drop(columns=list(df.select_dtypes(include=["object"]).columns))
        pca = PCA(n_components=n_components)
        components = pca.fit_transform(df)
        return pd.DataFrame(
            components, columns=[f"PC{i+1}" for i in range(n_components)]
        )

    @staticmethod
    def perform_tsne(df, n_components=2, perplexity=30.0, n_iter=1000):
        """
        Performs t-Distributed Stochastic Neighbor Embedding (t-SNE) on the data.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        n_components : int, optional
            The number of components to keep (default is 2).
        perplexity : float, optional
            The perplexity parameter for t-SNE (default is 30.0).
        n_iter : int, optional
            The number of iterations for optimization (default is 1000).

        Returns
        -------
        pandas.DataFrame
            The DataFrame with the t-SNE components.
        """
        df = df.drop(columns=list(df.select_dtypes(include=["object"]).columns))
        tsne = TSNE(n_components=n_components, perplexity=perplexity, n_iter=n_iter)
        components = tsne.fit_transform(df)
        return pd.DataFrame(
            components, columns=[f"t-SNE{i+1}" for i in range(n_components)]
        )

    @staticmethod
    def logistic_regression(df, target_column):
        """
        Performs logistic regression on the data.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        target_column : str
            The target column for classification.

        Returns
        -------
        dict
            The results of the logistic regression including accuracy, classification report, and confusion matrix.
        """
        X_train, X_test, y_train, y_test = Classification.preprocess_data(
            df, target_column
        )
        return Classification.logistic_regression(X_train, y_train, X_test, y_test)

    @staticmethod
    def decision_tree(df, target_column):
        """
        Performs decision tree classification on the data.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        target_column : str
            The target column for classification.

        Returns
        -------
        dict
            The results of the decision tree classification including accuracy, classification report, and confusion matrix.
        """
        X_train, X_test, y_train, y_test = Classification.preprocess_data(
            df, target_column
        )
        return Classification.decision_tree(X_train, y_train, X_test, y_test)

    @staticmethod
    def random_forest(df, target_column):
        """
        Performs random forest classification on the data.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        target_column : str
            The target column for classification.

        Returns
        -------
        dict
            The results of the random forest classification including accuracy, classification report, and confusion matrix.
        """
        X_train, X_test, y_train, y_test = Classification.preprocess_data(
            df, target_column
        )
        return Classification.random_forest(X_train, y_train, X_test, y_test)

    @staticmethod
    def linear_regression(df, target_column):
        """
        Performs linear regression on the data.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        target_column : str
            The target column for regression.

        Returns
        -------
        dict
            The results of the linear regression including mean squared error and R-squared score.
        """
        X_train, X_test, y_train, y_test = Regression.preprocess_data(df, target_column)
        return Regression.linear_regression(X_train, y_train, X_test, y_test)

    @staticmethod
    def ridge_regression(df, target_column, alpha=1.0):
        """
        Performs ridge regression on the data.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        target_column : str
            The target column for regression.
        alpha : float, optional
            Regularization strength (default is 1.0).

        Returns
        -------
        dict
            The results of the ridge regression including mean squared error and R-squared score.
        """
        X_train, X_test, y_train, y_test = Regression.preprocess_data(df, target_column)
        return Regression.ridge_regression(X_train, y_train, X_test, y_test, alpha)

    @staticmethod
    def lasso_regression(df, target_column, alpha=1.0):
        """
        Performs lasso regression on the data.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        target_column : str
            The target column for regression.
        alpha : float, optional
            Regularization strength (default is 1.0).

        Returns
        -------
        dict
            The results of the lasso regression including mean squared error and R-squared score.
        """
        X_train, X_test, y_train, y_test = Regression.preprocess_data(df, target_column)
        return Regression.lasso_regression(X_train, y_train, X_test, y_test, alpha)

    @staticmethod
    def decision_tree_regression(df, target_column):
        """
        Performs decision tree regression on the data.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        target_column : str
            The target column for regression.

        Returns
        -------
        dict
            The results of the decision tree regression including mean squared error and R-squared score.
        """
        X_train, X_test, y_train, y_test = Regression.preprocess_data(df, target_column)
        return Regression.decision_tree_regression(X_train, y_train, X_test, y_test)

    @staticmethod
    def random_forest_regression(df, target_column):
        """
        Performs random forest regression on the data.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        target_column : str
            The target column for regression.

        Returns
        -------
        dict
            The results of the random forest regression including mean squared error and R-squared score.
        """
        X_train, X_test, y_train, y_test = Regression.preprocess_data(df, target_column)
        return Regression.random_forest_regression(X_train, y_train, X_test, y_test)

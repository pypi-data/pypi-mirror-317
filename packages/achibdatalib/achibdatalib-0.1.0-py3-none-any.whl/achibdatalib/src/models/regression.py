import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score


class Regression:
    """
    A class used to perform regression analysis on data.

    Methods
    -------
    preprocess_data(df, target_column, test_size=0.2, scale_data=True)
        Preprocesses the data by splitting into training and testing sets and scaling if required.
    linear_regression(X_train, y_train, X_test, y_test)
        Performs linear regression on the data.
    ridge_regression(X_train, y_train, X_test, y_test, alpha=1.0)
        Performs ridge regression on the data.
    lasso_regression(X_train, y_train, X_test, y_test, alpha=1.0)
        Performs lasso regression on the data.
    decision_tree_regression(X_train, y_train, X_test, y_test)
        Performs decision tree regression on the data.
    random_forest_regression(X_train, y_train, X_test, y_test)
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
            The target column for regression.
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
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )

        if scale_data:
            scaler = StandardScaler()
            X_train = scaler.fit_transform(X_train)
            X_test = scaler.transform(X_test)

        return X_train, X_test, y_train, y_test

    @staticmethod
    def linear_regression(X_train, y_train, X_test, y_test):
        """
        Performs linear regression on the data.

        Parameters
        ----------
        X_train : array-like
            The training data.
        y_train : array-like
            The training labels.
        X_test : array-like
            The testing data.
        y_test : array-like
            The testing labels.

        Returns
        -------
        dict
            The results of the linear regression including mean squared error and R-squared score.
        """
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        results = {
            "mean_squared_error": mean_squared_error(y_test, y_pred),
            "r2_score": r2_score(y_test, y_pred),
        }

        return results

    @staticmethod
    def ridge_regression(X_train, y_train, X_test, y_test, alpha=1.0):
        """
        Performs ridge regression on the data.

        Parameters
        ----------
        X_train : array-like
            The training data.
        y_train : array-like
            The training labels.
        X_test : array-like
            The testing data.
        y_test : array-like
            The testing labels.
        alpha : float, optional
            Regularization strength (default is 1.0).

        Returns
        -------
        dict
            The results of the ridge regression including mean squared error and R-squared score.
        """
        model = Ridge(alpha=alpha)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        results = {
            "mean_squared_error": mean_squared_error(y_test, y_pred),
            "r2_score": r2_score(y_test, y_pred),
        }

        return results

    @staticmethod
    def lasso_regression(X_train, y_train, X_test, y_test, alpha=1.0):
        """
        Performs lasso regression on the data.

        Parameters
        ----------
        X_train : array-like
            The training data.
        y_train : array-like
            The training labels.
        X_test : array-like
            The testing data.
        y_test : array-like
            The testing labels.
        alpha : float, optional
            Regularization strength (default is 1.0).

        Returns
        -------
        dict
            The results of the lasso regression including mean squared error and R-squared score.
        """
        model = Lasso(alpha=alpha)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        results = {
            "mean_squared_error": mean_squared_error(y_test, y_pred),
            "r2_score": r2_score(y_test, y_pred),
        }

        return results

    @staticmethod
    def decision_tree_regression(X_train, y_train, X_test, y_test):
        """
        Performs decision tree regression on the data.

        Parameters
        ----------
        X_train : array-like
            The training data.
        y_train : array-like
            The training labels.
        X_test : array-like
            The testing data.
        y_test : array-like
            The testing labels.

        Returns
        -------
        dict
            The results of the decision tree regression including mean squared error and R-squared score.
        """
        model = DecisionTreeRegressor()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        results = {
            "mean_squared_error": mean_squared_error(y_test, y_pred),
            "r2_score": r2_score(y_test, y_pred),
        }

        return results

    @staticmethod
    def random_forest_regression(X_train, y_train, X_test, y_test):
        """
        Performs random forest regression on the data.

        Parameters
        ----------
        X_train : array-like
            The training data.
        y_train : array-like
            The training labels.
        X_test : array-like
            The testing data.
        y_test : array-like
            The testing labels.

        Returns
        -------
        dict
            The results of the random forest regression including mean squared error and R-squared score.
        """
        model = RandomForestRegressor()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        results = {
            "mean_squared_error": mean_squared_error(y_test, y_pred),
            "r2_score": r2_score(y_test, y_pred),
        }

        return results

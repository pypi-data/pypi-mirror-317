import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


class Classification:
    """
    A class used to perform classification and clustering on data.

    Methods
    -------
    preprocess_data(df, target_column, test_size=0.2, scale_data=True)
        Preprocesses the data by splitting into training and testing sets and scaling if required.
    logistic_regression(X_train, y_train, X_test, y_test)
        Performs logistic regression on the data.
    decision_tree(X_train, y_train, X_test, y_test)
        Performs decision tree classification on the data.
    random_forest(X_train, y_train, X_test, y_test)
        Performs random forest classification on the data.
    kmeans_clustering(df, n_clusters)
        Performs KMeans clustering on the data.
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
            The target column for classification.
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
        # print("ssss", df)
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
    def logistic_regression(X_train, y_train, X_test, y_test):
        """
        Performs logistic regression on the data.

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
            The results of the logistic regression including accuracy, classification report, and confusion matrix.
        """
        model = LogisticRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        results = {
            "accuracy": accuracy_score(y_test, y_pred),
            "classification_report": classification_report(y_test, y_pred),
            "confusion_matrix": confusion_matrix(y_test, y_pred),
        }

        return results

    @staticmethod
    def decision_tree(X_train, y_train, X_test, y_test):
        """
        Performs decision tree classification on the data.

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
            The results of the decision tree classification including accuracy, classification report, and confusion matrix.
        """
        model = DecisionTreeClassifier()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        results = {
            "accuracy": accuracy_score(y_test, y_pred),
            "classification_report": classification_report(y_test, y_pred),
            "confusion_matrix": confusion_matrix(y_test, y_pred),
        }

        return results

    @staticmethod
    def random_forest(X_train, y_train, X_test, y_test):
        """
        Performs random forest classification on the data.

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
            The results of the random forest classification including accuracy, classification report, and confusion matrix.
        """
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        results = {
            "accuracy": accuracy_score(y_test, y_pred),
            "classification_report": classification_report(y_test, y_pred),
            "confusion_matrix": confusion_matrix(y_test, y_pred),
        }

        return results

    @staticmethod
    def kmeans_clustering(df, n_clusters):
        """
        Performs KMeans clustering on the data.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data.
        n_clusters : int
            The number of clusters to form.

        Returns
        -------
        dict
            The results of the KMeans clustering including cluster centers and labels.
        """
        model = KMeans(n_clusters=n_clusters, random_state=42)
        df_scaled = StandardScaler().fit_transform(df)
        model.fit(df_scaled)

        results = {"cluster_centers": model.cluster_centers_, "labels": model.labels_}

        return results

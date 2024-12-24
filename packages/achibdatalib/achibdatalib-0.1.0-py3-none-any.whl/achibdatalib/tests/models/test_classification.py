import pytest
import pandas as pd
from src.models.classification import Classification


@pytest.fixture
def sample_data():
    data = {"A": [1, 2, 3, 4, 5], "B": [5, 6, 7, 8, 9], "C": [0, 1, 0, 1, 0]}
    return pd.DataFrame(data)


@pytest.fixture
def sample_data_for_clustering():
    data = {"A": [1, 2, 3, 4, 5], "B": [5, 6, 7, 8, 9]}
    return pd.DataFrame(data)


def test_preprocess_data(sample_data):
    X_train, X_test, y_train, y_test = Classification.preprocess_data(
        sample_data, target_column="C"
    )
    assert X_train.shape[0] + X_test.shape[0] == sample_data.shape[0]
    assert y_train.shape[0] + y_test.shape[0] == sample_data.shape[0]


def test_logistic_regression(sample_data):
    X_train, X_test, y_train, y_test = Classification.preprocess_data(
        sample_data, target_column="C"
    )
    results = Classification.logistic_regression(X_train, y_train, X_test, y_test)
    assert "accuracy" in results
    assert "classification_report" in results
    assert "confusion_matrix" in results


def test_decision_tree(sample_data):
    X_train, X_test, y_train, y_test = Classification.preprocess_data(
        sample_data, target_column="C"
    )
    results = Classification.decision_tree(X_train, y_train, X_test, y_test)
    assert "accuracy" in results
    assert "classification_report" in results
    assert "confusion_matrix" in results


def test_random_forest(sample_data):
    X_train, X_test, y_train, y_test = Classification.preprocess_data(
        sample_data, target_column="C"
    )
    results = Classification.random_forest(X_train, y_train, X_test, y_test)
    assert "accuracy" in results
    assert "classification_report" in results
    assert "confusion_matrix" in results


def test_kmeans_clustering(sample_data_for_clustering):
    results = Classification.kmeans_clustering(sample_data_for_clustering, n_clusters=2)
    assert "cluster_centers" in results
    assert "labels" in results

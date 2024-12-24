import pytest
import pandas as pd
from src.models.regression import Regression


@pytest.fixture
def sample_data():
    data = {"A": [1, 2, 3, 4, 5], "B": [5, 6, 7, 8, 9], "C": [10, 20, 30, 40, 50]}
    return pd.DataFrame(data)


def test_preprocess_data(sample_data):
    X_train, X_test, y_train, y_test = Regression.preprocess_data(
        sample_data, target_column="C"
    )
    assert X_train.shape[0] + X_test.shape[0] == sample_data.shape[0]
    assert y_train.shape[0] + y_test.shape[0] == sample_data.shape[0]


def test_linear_regression(sample_data):
    X_train, X_test, y_train, y_test = Regression.preprocess_data(
        sample_data, target_column="C"
    )
    results = Regression.linear_regression(X_train, y_train, X_test, y_test)
    assert "mean_squared_error" in results
    assert "r2_score" in results


def test_ridge_regression(sample_data):
    X_train, X_test, y_train, y_test = Regression.preprocess_data(
        sample_data, target_column="C"
    )
    results = Regression.ridge_regression(X_train, y_train, X_test, y_test, alpha=1.0)
    assert "mean_squared_error" in results
    assert "r2_score" in results


def test_lasso_regression(sample_data):
    X_train, X_test, y_train, y_test = Regression.preprocess_data(
        sample_data, target_column="C"
    )
    results = Regression.lasso_regression(X_train, y_train, X_test, y_test, alpha=1.0)
    assert "mean_squared_error" in results
    assert "r2_score" in results


def test_decision_tree_regression(sample_data):
    X_train, X_test, y_train, y_test = Regression.preprocess_data(
        sample_data, target_column="C"
    )
    results = Regression.decision_tree_regression(X_train, y_train, X_test, y_test)
    assert "mean_squared_error" in results
    assert "r2_score" in results


def test_random_forest_regression(sample_data):
    X_train, X_test, y_train, y_test = Regression.preprocess_data(
        sample_data, target_column="C"
    )
    results = Regression.random_forest_regression(X_train, y_train, X_test, y_test)
    assert "mean_squared_error" in results
    assert "r2_score" in results

import pytest
import pandas as pd
from src.analysis.advanced_analysis import AdvancedAnalysis


@pytest.fixture
def sample_data():
    data = {"A": [1, 2, 3, 4, 5], "B": [5, 6, 7, 8, 9], "C": [10, 20, 30, 40, 50]}
    return pd.DataFrame(data)


@pytest.fixture
def sample_data_classification():
    data = {"A": [1, 2, 3, 4, 5], "B": [5, 6, 7, 8, 9], "C": [0, 1, 0, 1, 0]}
    return pd.DataFrame(data)


def test_preprocess_data(sample_data):
    X_train, X_test, y_train, y_test = AdvancedAnalysis.preprocess_data(
        sample_data, target_column="C"
    )
    assert X_train.shape[0] + X_test.shape[0] == sample_data.shape[0]
    assert y_train.shape[0] + y_test.shape[0] == sample_data.shape[0]


def test_perform_pca(sample_data):
    pca_result = AdvancedAnalysis.perform_pca(sample_data, n_components=2)
    assert pca_result.shape[1] == 2


def test_perform_tsne(sample_data):
    tsne_result = AdvancedAnalysis.perform_tsne(sample_data, n_components=2)
    assert tsne_result.shape[1] == 2


def test_logistic_regression(sample_data_classification):
    results = AdvancedAnalysis.logistic_regression(
        sample_data_classification, target_column="C"
    )
    assert "accuracy" in results
    assert "classification_report" in results
    assert "confusion_matrix" in results


def test_decision_tree(sample_data_classification):
    results = AdvancedAnalysis.decision_tree(
        sample_data_classification, target_column="C"
    )
    assert "accuracy" in results
    assert "classification_report" in results
    assert "confusion_matrix" in results


def test_random_forest(sample_data_classification):
    results = AdvancedAnalysis.random_forest(
        sample_data_classification, target_column="C"
    )
    assert "accuracy" in results
    assert "classification_report" in results
    assert "confusion_matrix" in results


def test_linear_regression(sample_data):
    results = AdvancedAnalysis.linear_regression(sample_data, target_column="C")
    assert "mean_squared_error" in results
    assert "r2_score" in results


def test_ridge_regression(sample_data):
    results = AdvancedAnalysis.ridge_regression(
        sample_data, target_column="C", alpha=1.0
    )
    assert "mean_squared_error" in results
    assert "r2_score" in results


def test_lasso_regression(sample_data):
    results = AdvancedAnalysis.lasso_regression(
        sample_data, target_column="C", alpha=1.0
    )
    assert "mean_squared_error" in results
    assert "r2_score" in results


def test_decision_tree_regression(sample_data):
    results = AdvancedAnalysis.decision_tree_regression(sample_data, target_column="C")
    assert "mean_squared_error" in results
    assert "r2_score" in results


def test_random_forest_regression(sample_data):
    results = AdvancedAnalysis.random_forest_regression(sample_data, target_column="C")
    assert "mean_squared_error" in results
    assert "r2_score" in results

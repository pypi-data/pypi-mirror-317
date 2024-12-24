import pytest
import pandas as pd
from src.data_lib import DataLib


@pytest.fixture
def sample_data():
    data = {"A": [1, 2, 3, 4, 5], "B": [5, 6, 7, 8, 9], "C": [10, 20, 30, 40, 50]}
    return pd.DataFrame(data)


@pytest.fixture
def sample_data_classification():
    data = {"A": [1, 2, 3, 4, 5], "B": [5, 6, 7, 8, 9], "C": [0, 1, 0, 1, 0]}
    return pd.DataFrame(data)


def test_load_and_clean_data(sample_data):
    cleaned_data = DataLib.load_and_clean_data(sample_data, cleaning_strategy="drop")
    assert not cleaned_data.isnull().values.any()


def test_describe_data(sample_data):
    description = DataLib.describe_data(sample_data)
    assert "mean" in description.index


def test_visualize_data(sample_data):
    # This test is a placeholder as visualizations are typically not tested this way
    try:
        DataLib.visualize_data(sample_data, "A")
        assert True
    except Exception:
        assert False


def test_perform_classification(sample_data_classification):
    results = DataLib.perform_classification(sample_data_classification, "C")
    assert "accuracy" in results
    assert "classification_report" in results
    assert "confusion_matrix" in results


def test_perform_regression(sample_data):
    results = DataLib.perform_regression(sample_data, "C")
    assert "mean_squared_error" in results
    assert "r2_score" in results


def test_perform_advanced_analysis(sample_data):
    results = DataLib.perform_advanced_analysis(sample_data, "C")
    assert "explained_variance_ratio_" in results


def test_analyze_data_engine(sample_data_classification):
    results = DataLib.analyze_data_engine(sample_data_classification, "C")
    assert "description" in results
    assert "classification_results" in results
    assert "regression_results" in results
    assert "advanced_analysis_results" in results

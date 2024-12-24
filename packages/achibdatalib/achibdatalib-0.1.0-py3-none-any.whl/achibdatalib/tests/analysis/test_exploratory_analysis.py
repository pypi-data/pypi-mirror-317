import pytest
import pandas as pd
from src.analysis.exploratory_analysis import ExploratoryAnalysis


@pytest.fixture
def sample_data():
    data = {
        "A": [1, 2, 3, 4, 5],
        "B": [5, 6, 7, 8, 9],
        "C": ["cat", "dog", "cat", "dog", "cat"],
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_data_with_nan():
    data = {
        "A": [1, 2, None, 4, 5],
        "B": [5, None, 7, 8, 9],
        "C": ["cat", "dog", "cat", "dog", "cat"],
    }
    return pd.DataFrame(data)


def test_load_and_clean_data(sample_data):
    df = ExploratoryAnalysis.load_and_clean_data(sample_data)
    assert isinstance(df, pd.DataFrame)
    assert df.isnull().sum().sum() == 0


def test_describe_and_visualize_data(sample_data):
    ExploratoryAnalysis.describe_and_visualize_data(sample_data)
    # No assertion needed as this function prints and plots


def test_analyze_correlations(sample_data):
    ExploratoryAnalysis.analyze_correlations(sample_data)
    # No assertion needed as this function prints and plots


def test_perform_statistical_tests(sample_data):
    ExploratoryAnalysis.perform_statistical_tests(sample_data, "A", "B")
    # No assertion needed as this function prints results


def test_visualize_distributions(sample_data):
    ExploratoryAnalysis.visualize_distributions(sample_data, ["A", "B"])
    # No assertion needed as this function plots

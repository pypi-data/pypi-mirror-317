import pytest
import pandas as pd
import numpy as np
from src.statistics import Statistics


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
        "A": [1, 2, np.nan, 4, 5],
        "B": [5, np.nan, 7, 8, 9],
        "C": ["cat", "dog", "cat", "dog", "cat"],
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_data_for_corr():
    data = {"A": [1, 2, 3, 4, 5], "B": [2, 4, 6, 8, 10], "C": [5, 4, 3, 2, 1]}
    return pd.DataFrame(data)


def test_describe_data(sample_data):
    desc = Statistics.describe_data(sample_data)
    assert "mean" in desc.index


def test_correlation_matrix(sample_data_for_corr):
    corr = Statistics.correlation_matrix(sample_data_for_corr)
    assert corr.loc["A", "B"] == 1.0
    assert corr.loc["A", "C"] == -1.0


def test_t_test():
    sample1 = [1, 2, 3, 4, 5]
    sample2 = [2, 3, 4, 5, 6]
    t_stat, p_value = Statistics.t_test(sample1, sample2)
    assert p_value > 0.05


def test_chi_square_test():
    observed = [10, 20, 30]
    expected = [10, 20, 30]
    chi2_stat, p_value = Statistics.chi_square_test(observed, expected)
    assert p_value == 1.0


def test_anova():
    sample1 = [1, 2, 3, 4, 5]
    sample2 = [2, 3, 4, 5, 6]
    sample3 = [3, 4, 5, 6, 7]
    f_stat, p_value = Statistics.anova(sample1, sample2, sample3)
    assert p_value > 0.05


def test_linear_regression():
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]
    slope, intercept, r_value, p_value, std_err = Statistics.linear_regression(x, y)
    assert slope == 2.0
    assert intercept == 0.0


def test_z_score(sample_data):
    z_scores = Statistics.z_score(sample_data, "A")
    assert np.allclose(z_scores.mean(), 0)
    assert np.allclose(z_scores.std(), 1)


def test_moving_average(sample_data):
    moving_avg = Statistics.moving_average(sample_data, "A", window=2)
    assert len(moving_avg) == len(sample_data)
    assert np.isnan(moving_avg.iloc[0])

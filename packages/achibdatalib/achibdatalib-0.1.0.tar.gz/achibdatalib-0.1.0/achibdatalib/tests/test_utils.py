import pytest
import pandas as pd
import numpy as np
from src.utils import Utils


@pytest.fixture
def sample_data():
    data = {"A": [1, 2, 3, 4, 5], "B": [5, 6, 7, 8, 9], "C": [10, 20, 30, 40, 50]}
    return pd.DataFrame(data)


@pytest.fixture
def sample_array():
    return np.array([1, 2, 3, 4, 5])


def test_calculate_mean(sample_data):
    mean = Utils.calculate_mean(sample_data, "A")
    assert mean == 3


def test_calculate_sum(sample_data):
    total_sum = Utils.calculate_sum(sample_data, "A")
    assert total_sum == 15


def test_calculate_max(sample_data):
    max_value = Utils.calculate_max(sample_data, "A")
    assert max_value == 5


def test_calculate_min(sample_data):
    min_value = Utils.calculate_min(sample_data, "A")
    assert min_value == 1


def test_calculate_std(sample_data):
    std_dev = Utils.calculate_std(sample_data, "A")
    assert np.isclose(std_dev, 1.5811, atol=1e-4)


def test_normalize_array(sample_array):
    normalized_array = Utils.normalize_array(sample_array)
    expected_array = np.array([0, 0.25, 0.5, 0.75, 1])
    assert np.allclose(normalized_array, expected_array)


def test_calculate_median(sample_data):
    median = Utils.calculate_median(sample_data, "A")
    assert median == 3


def test_calculate_variance(sample_data):
    variance = Utils.calculate_variance(sample_data, "A")
    assert np.isclose(variance, 2.5, atol=1e-4)


def test_calculate_mode(sample_data):
    mode = Utils.calculate_mode(sample_data, "A")
    assert mode == 1


def test_calculate_iqr(sample_data):
    iqr = Utils.calculate_iqr(sample_data, "A")
    assert iqr == 2

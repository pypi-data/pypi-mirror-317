import pytest
import pandas as pd
import numpy as np
from src.data_processing import DataProcessor


@pytest.fixture
def sample_data():
    data = {
        "A": [1, 2, np.nan, 4, 5],
        "B": [5, np.nan, np.nan, 8, 10],
        "C": ["cat", "dog", "cat", "dog", "cat"],
        "D": [1, 2, 3, 4, 5],
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_data_2():
    data = {
        "A": [1, 2, 3, 4, 5],
        "B": [5, 6, 7, 8, 9],
        "C": ["cat", "dog", "cat", "dog", "cat"],
    }
    return pd.DataFrame(data)


def test_load_data(sample_data):
    df = DataProcessor.load_data(sample_data)
    assert isinstance(df, pd.DataFrame)


def test_clean_data(sample_data):
    df = DataProcessor.clean_data(sample_data, strategy="drop")
    assert df.isnull().sum().sum() == 0


def test_transform_data(sample_data):
    df = DataProcessor.transform_data(
        sample_data, columns=["A", "B"], method="standard"
    )
    # Fill NaN values with the mean before calculating mean and std
    df["A"] = df["A"].fillna(df["A"].mean())
    assert np.allclose(df["A"].mean(), 0, equal_nan=True)
    assert np.allclose(df["A"].std(), 1, equal_nan=True)


def test_normalize_data(sample_data):
    df = DataProcessor.normalize_data(sample_data, columns=["A", "B"])
    # Fill NaN values with the mean before calculating mean and std
    df["A"] = df["A"].fillna(df["A"].mean())
    assert np.allclose(df["A"].mean(), 0, equal_nan=True)
    assert np.allclose(df["A"].std(), 1, equal_nan=True)


def test_bin_data(sample_data):
    df = DataProcessor.bin_data(
        sample_data, column="D", bins=[0, 2, 4, 6], labels=["low", "medium", "high"]
    )
    assert df["D"].dtype.name == "category"


def test_impute_missing_values(sample_data):
    df = DataProcessor.impute_missing_values(sample_data, strategy="mean")
    assert df.isnull().sum().sum() == 0


def test_encode_categorical(sample_data):
    df = DataProcessor.encode_categorical(sample_data, columns=["C"])
    assert "C_cat" in df.columns
    assert "C_dog" in df.columns


def test_handle_outliers(sample_data):
    df = DataProcessor.handle_outliers(sample_data, columns=["A", "B"], method="iqr")
    assert df.shape[0] <= sample_data.shape[0]


def test_split_data(sample_data):
    X_train, X_test, y_train, y_test = DataProcessor.split_data(
        sample_data, target_column="D", test_size=0.2
    )
    assert len(X_train) + len(X_test) == len(sample_data)


def test_aggregate_data(sample_data):
    df = DataProcessor.aggregate_data(
        sample_data, group_by_columns=["C"], agg_funcs={"A": "mean", "B": "sum"}
    )
    assert "A" in df.columns
    assert "B" in df.columns


def test_merge_data(sample_data, sample_data_2):
    df = DataProcessor.merge_data(sample_data, sample_data_2, on="A", how="inner")
    assert "A" in df.columns
    assert "B_x" in df.columns
    assert "B_y" in df.columns


def test_pivot_data(sample_data):
    df = DataProcessor.pivot_data(sample_data, index="A", columns="C", values="B")
    assert "cat" in df.columns
    assert "dog" in df.columns


def test_filter_data(sample_data):
    df = DataProcessor.filter_data(sample_data, condition="A > 2")
    assert df.shape[0] < sample_data.shape[0]


def test_save_data(sample_data, tmpdir):
    file_path = tmpdir.join("test.csv")
    DataProcessor.save_data(sample_data, file_path)
    assert file_path.exists()


def test_apply_function(sample_data):
    df = DataProcessor.apply_function(
        sample_data.select_dtypes(include=[np.number]),
        func=lambda x: x.fillna(x.mean()),
        axis=0,
    )
    assert not df.isnull().values.any()


def test_map_values(sample_data):
    df = DataProcessor.map_values(
        sample_data, column="C", mapping={"cat": "feline", "dog": "canine"}
    )
    assert "feline" in df["C"].values
    assert "canine" in df["C"].values

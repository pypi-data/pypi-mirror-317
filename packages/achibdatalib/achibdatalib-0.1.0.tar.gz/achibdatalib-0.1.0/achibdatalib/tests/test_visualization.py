import pytest
import pandas as pd
import matplotlib.pyplot as plt
from src.visualization import Visualizations


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


def test_plot_histogram(sample_data):
    Visualizations.plot_histogram(sample_data, column="A")
    plt.close()


def test_plot_scatter(sample_data):
    Visualizations.plot_scatter(sample_data, x="A", y="B")
    plt.close()


def test_plot_boxplot(sample_data):
    Visualizations.plot_boxplot(sample_data, column="A")
    plt.close()


def test_plot_heatmap(sample_data):
    Visualizations.plot_heatmap(sample_data)
    plt.close()


def test_plot_line(sample_data):
    Visualizations.plot_line(sample_data, x="A", y="B")
    plt.close()


def test_plot_bar(sample_data):
    Visualizations.plot_bar(sample_data, x="C", y="A")
    plt.close()


def test_plot_pie(sample_data):
    Visualizations.plot_pie(sample_data, column="C")
    plt.close()


def test_plot_pairplot(sample_data):
    Visualizations.plot_pairplot(sample_data, hue="C")
    plt.close()


def test_plot_violin(sample_data):
    Visualizations.plot_violin(sample_data, x="C", y="A")
    plt.close()

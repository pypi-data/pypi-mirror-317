import pandas as pd
from src.data_lib import DataLib
import numpy as np


# data = pd.DataFrame(
#     {"A": [1, 2, 3, 4, 5], "B": [5, 6, 7, 8, 9], "C": [10, 20, 30, 40, 50]}
# )
data = pd.DataFrame(
    {
        "A": [1, 2, np.nan, 4, 5],
        "B": [5, np.nan, np.nan, 8, 10],
        "C": ["cat", "dog", "cat", "dog", "cat"],
        "D": [1, 2, 3, 4, 5],
    }
)

# Load and clean data
df = DataLib.load_and_clean_data("test2.csv")

print(df.columns)
# Describe data
description = DataLib.describe_data(df)
print(description)

# Visualize data
DataLib.visualize_data(df, "A")


# Perform classification
classification_results = DataLib.perform_classification(df, "A")
print(classification_results)

# Perform regression
regression_results = DataLib.perform_regression(df, "A")
print(regression_results)

# Perform advanced analysis
advanced_analysis_results = DataLib.perform_advanced_analysis(df, "A")
print(advanced_analysis_results)

# Execute full analysis workflow
results = DataLib.analyze_data_engine(data, "A")
print("ddddddd", results)

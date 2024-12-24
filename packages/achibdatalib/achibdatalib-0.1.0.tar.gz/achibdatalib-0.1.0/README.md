# DataLib

A library for data manipulation and analysis.

DataLib is a comprehensive data analysis library that provides functionalities for data loading, cleaning, processing, visualization, classification, regression, and advanced analysis.

## Installation

You can install DataLib using `pip`:

```sh
pip install achibdatalib
```

## Dependencies

DataLib requires the following dependencies:

- pandas>=1.3.0
- numpy>=1.21.0,<2.0.0
- scikit-learn>=0.24.2
- pytest>=6.2.4

## Usage

Here is an example of how to use DataLib:

```python
import pandas as pd
from DataLib.data_lib import DataLib

# Load and clean data
df = DataLib.load_and_clean_data('data.csv')

# Describe data
description = DataLib.describe_data(df)
print(description)

# Visualize data
DataLib.visualize_data(df, 'column_name')

# Perform classification
classification_results = DataLib.perform_classification(df, 'target_column')
print(classification_results)

# Perform regression
regression_results = DataLib.perform_regression(df, 'target_column')
print(regression_results)

# Perform advanced analysis
advanced_analysis_results = DataLib.perform_advanced_analysis(df, 'target_column')
print(advanced_analysis_results)

# Execute full analysis workflow
results = DataLib.analyze_data_engine('data.csv', 'target_column')
print(results)
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License.

# Explorytics Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
   - [Installation](#installation)
3. [Key Components](#key-components)
   - [DataAnalyzer](#dataanalyzer)
   - [Visualizer](#visualizer)
4. [Usage Examples](#usage-examples)
   - [Dataset Preparation](#dataset-preparation)
   - [Comprehensive Analysis](#comprehensive-analysis)
   - [Visualization](#visualization)
5. [API Reference](#api-reference)
6. [Contributing](#contributing)
7. [License](#license)

## Introduction

**Explorytics** is a Python library designed to simplify exploratory data analysis (EDA). It automates statistical evaluations, visualizations, and key insights extraction, providing an intuitive interface for analyzing complex datasets quickly and effectively.

---

## Getting Started

### Installation

#### Prerequisites

- Python 3.8 or higher
- Recommended: Jupyter Notebook for interactive exploration

#### Installation Steps

Install Explorytics via pip:

```bash
pip install explorytics
```

To upgrade an existing installation:

```bash
pip install --upgrade explorytics
```

---

## Key Components

### DataAnalyzer

`DataAnalyzer` is the primary interface for analyzing datasets.

#### Initialization

```python
from explorytics import DataAnalyzer

analyzer = DataAnalyzer(dataframe)
```

#### Key Features

1. **Statistical Analysis**: Computes numeric summaries, including mean, median, standard deviation, and percentiles.
2. **Correlation Analysis**: Identifies relationships between variables.
3. **Outlier Detection**: Detects outliers based on statistical thresholds.

---

### Visualizer

The `Visualizer` submodule provides tools for creating plots.

#### Common Visualizations

- **Distribution Plots**:

  ```python
  analyzer.visualizer.plot_distribution(feature_name, kde=True)
  ```

- **Correlation Heatmaps**:

  ```python
  analyzer.visualizer.plot_correlation_matrix()
  ```

- **Scatter Plots**:

  ```python
  analyzer.visualizer.plot_scatter(x, y, color="column_name")
  ```

- **Box Plots**:

  ```python
  analyzer.visualizer.plot_boxplot(feature_name)
  ```

---

## Usage Examples

### Dataset Preparation

1. **Load the dataset**:

   ```python
   import pandas as pd
   from sklearn.datasets import load_wine

   # Load the wine dataset
   wine = load_wine()
   df = pd.DataFrame(wine.data, columns=wine.feature_names)
   df['wine_class'] = wine.target
   ```

2. **Initialize the analyzer**:

   ```python
   from explorytics import DataAnalyzer

   analyzer = DataAnalyzer(df)
   ```

### Comprehensive Analysis

1. **Perform analysis**:

   ```python
   results = analyzer.analyze()
   ```

2. **Display basic statistics**:

   ```python
   print("Basic Statistics:")
   print(results.basic_stats)
   ```

3. **Identify correlations**:

   ```python
   print("Correlations:")
   print(results.correlations)
   ```

4. **Analyze outliers**:

   ```python
   print("Outlier Information:")
   print(results.outliers)
   ```

### Visualization

1. **Plot feature distribution**:

   ```python
   analyzer.visualizer.plot_distribution('alcohol', kde=True).show()
   ```

2. **Plot correlation matrix**:

   ```python
   analyzer.visualizer.plot_correlation_matrix().show()
   ```

3. **Visualize scatter relationships**:

   ```python
   analyzer.visualizer.plot_scatter('alcohol', 'color_intensity', color='wine_class').show()
   ```

4. **Create a boxplot for outliers**:

   ```python
   analyzer.visualizer.plot_boxplot('malic_acid').show()
   ```

---

## API Reference

### `DataAnalyzer`

#### Initialization

```python
DataAnalyzer(dataframe)
```

- **Parameters**:
  - `dataframe` (*pandas.DataFrame*): Dataset to analyze.

#### Methods

- **`analyze()`**:
  Performs comprehensive analysis, returning:
  - `basic_stats`: Summary statistics for numeric columns.
  - `correlations`: Pairwise correlation matrix.
  - `outliers`: Information on detected outliers.

- **`get_feature_summary(feature_name)`**:
  Returns detailed statistics for a specific feature.

### `Visualizer`

#### Methods

- **`plot_distribution(feature_name, kde=False)`**:
  Plots the distribution of a feature.

- **`plot_correlation_matrix()`**:
  Displays a heatmap of correlations.

- **`plot_scatter(x, y, color=None)`**:
  Creates a scatter plot for two features.

- **`plot_boxplot(feature_name)`**:
  Generates a boxplot for a feature.

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch:

   ```bash
   git checkout -b feature-name
   ```

3. Submit a pull request.

---

## License

Explorytics is licensed under the MIT License. See [LICENSE](LICENSE) for details.

# Explorytics

Explorytics is a Python library designed to simplify the process of exploratory data analysis (EDA). With an intuitive interface and powerful visualization tools, it provides quick insights into datasets, helping you understand distributions, correlations, and outliers with ease.

## Features

- **Comprehensive Data Analysis**: Perform statistical and visual analysis in a few lines of code.
- **Interactive Visualizations**: Generate dynamic plots for distributions, correlations, and relationships.
- **Outlier Detection**: Identify and explore outliers across various features.
- **User-Friendly API**: Designed for simplicity and ease of use, even for beginners.

## Installation

Install Explorytics using pip:

```bash
pip install explorytics
```

## Getting Started

Here's a quick example of how to use Explorytics with the Wine dataset from scikit-learn:

```python
# Import required libraries
import pandas as pd
from sklearn.datasets import load_wine
from explorytics import DataAnalyzer

# Load the wine dataset
wine = load_wine()
df = pd.DataFrame(wine.data, columns=wine.feature_names)
df['wine_class'] = wine.target

# Initialize the analyzer
analyzer = DataAnalyzer(df)

# Perform analysis
results = analyzer.analyze()

# Generate a distribution plot
analyzer.visualizer.plot_distribution('alcohol', kde=True).show()

# Generate a correlation heatmap
analyzer.visualizer.plot_correlation_matrix().show()
```

## Documentation

The complete documentation is available [here](./DOCUMENTATION.md). It includes details on:

- Installation and setup
- Usage examples
- API references for key classes and methods
- Advanced configuration options

## Examples

Explore the `examples` folder for Jupyter notebooks showcasing various use cases, including:

- Basic data exploration
- Advanced feature relationships
- Outlier detection and analysis

## Contributing

We welcome contributions! If you'd like to contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make your changes and commit: `git commit -m 'Add feature name'`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.

Please ensure your code adheres to the existing style and includes tests for any new functionality.

## License

Explorytics is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.

## Acknowledgments

This library was inspired by a course I was pursuing on Coursera: [Exploratory Data Analysis for Machine Learning](https://www.coursera.org/learn/ibm-exploratory-data-analysis-for-machine-learning/). Special thanks to the open-source community for providing inspiration and support.

---

Start exploring your data today with Explorytics!

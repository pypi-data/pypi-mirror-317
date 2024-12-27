![clustermatic](https://raw.githubusercontent.com/AKapich/clustermatic/refs/heads/main/clustermatic/auxiliary/clustermatic.png)

# clustermatic

`clustermatic` is a Python library designed to accelerate clustering tasks using `scikit-learn`. It serves as a quick tool for selecting the optimal clustering algorithm and its hyperparameters, providing visualizations and metrics for comparison.

## Features

- **Clustering Algorithms**: Analyzes six clustering algorithms from `scikit-learn`:
    - `KMeans`
    - `DBSCAN`
    - `MiniBatchKMeans`
    - `AgglomerativeClustering`
    - `OPTICS`
    - `SpectralClustering`
- **Optimization Methods**: Includes Bayesian optimization and random search for hyperparameter tuning.
- **Flexible Preprocessing**: Allows users to customize how the data is meant to be preprocessed, adjusting methods such as scaling, normalization, and dimensionality reduction.
- **Evaluation Metrics**: Supports evaluation with `silhouette`, `calinski_harabasz`, and `davies_bouldin` scores.
- **Report Generation**: Generates reports in HTML format after optimization.

## Installation

To install `clustermatic`, use pip:

```bash
pip install clustermatic
```




from sklearn.metrics import (
    silhouette_score,
    davies_bouldin_score,
    calinski_harabasz_score,
)

score_metric_values = {
    "silhouette": -1,
    "calinski_harabasz": 0,
    "davies_bouldin": 999999,
}


def cluster_scorer(estimator, X, score_func, default_value):
    labels = estimator.fit_predict(X)
    if len(set(labels)) > 1:
        return score_func(X, labels)
    else:
        return default_value


def silhouette_scorer(estimator, X):
    return cluster_scorer(
        estimator, X, silhouette_score, score_metric_values["silhouette"]
    )


def davies_bouldin_scorer(estimator, X):
    return cluster_scorer(
        estimator, X, davies_bouldin_score, score_metric_values["davies_bouldin"]
    )


def calinski_harabasz_scorer(estimator, X):
    return cluster_scorer(
        estimator, X, calinski_harabasz_score, score_metric_values["calinski_harabasz"]
    )

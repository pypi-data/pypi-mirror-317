from sklearn.cluster import (
    KMeans,
    DBSCAN,
    MiniBatchKMeans,
    AgglomerativeClustering,
    SpectralClustering,
    OPTICS,
)
from skopt.space import Integer, Real, Categorical
from scipy.stats import uniform, randint


search_spaces_bayes = {
    KMeans: {
        "n_clusters": Integer(2, 10),
        "init": Categorical(["k-means++", "random"]),
        "n_init": Integer(10, 20),
        "tol": Real(1e-4, 1e-2, prior="log-uniform"),
    },
    DBSCAN: {
        "eps": Real(0.1, 10.0, prior="uniform"),
        "min_samples": Integer(2, 20),
        "metric": Categorical(["euclidean", "manhattan", "cosine"]),
    },
    MiniBatchKMeans: {
        "n_clusters": Integer(2, 10),
        "init": Categorical(["k-means++", "random"]),
        "n_init": Integer(10, 20),
        "tol": Real(1e-4, 1e-2, prior="log-uniform"),
        "max_iter": Integer(100, 300),
        "batch_size": Integer(10, 100),
    },
    AgglomerativeClustering: {
        "n_clusters": Integer(2, 10),
        "metric": Categorical(["euclidean", "l1", "l2", "manhattan", "cosine"]),
        "linkage": Categorical(["complete", "average", "single"]),
    },
    OPTICS: {
        "min_samples": Integer(2, 20),
        "xi": Real(0.01, 0.5, prior="uniform"),
        "min_cluster_size": Real(0.01, 0.5, prior="uniform"),
    },
    SpectralClustering: {
        "n_clusters": Integer(2, 10),
        "eigen_solver": Categorical(["arpack", "lobpcg", "amg"]),
        "affinity": Categorical(["nearest_neighbors", "rbf"]),
        "n_init": Integer(10, 20),
        "assign_labels": Categorical(["kmeans", "discretize"]),
    },
}

search_spaces_random = {
    KMeans: {
        "n_clusters": randint(2, 11),
        "init": ["k-means++", "random"],
        "n_init": randint(10, 21),
        "tol": uniform(1e-4, 1e-2 - 1e-4),
    },
    DBSCAN: {
        "eps": uniform(0.1, 10.0 - 0.1),
        "min_samples": randint(2, 21),
        "metric": ["euclidean", "manhattan", "cosine"],
    },
    MiniBatchKMeans: {
        "n_clusters": randint(2, 11),
        "init": ["k-means++", "random"],
        "n_init": randint(10, 21),
        "tol": uniform(1e-4, 1e-2 - 1e-4),
        "max_iter": randint(100, 301),
        "batch_size": randint(10, 101),
    },
    AgglomerativeClustering: {
        "n_clusters": randint(2, 11),
        "metric": [
            "euclidean",
            "l1",
            "l2",
            "manhattan",
            "cosine",
        ],
        "linkage": ["complete", "average", "single"],
    },
    OPTICS: {
        "min_samples": randint(2, 21),
        "xi": uniform(0.01, 0.5 - 0.01),
        "min_cluster_size": uniform(0.01, 0.5 - 0.01),
    },
    SpectralClustering: {
        "n_clusters": randint(2, 11),
        "eigen_solver": ["arpack", "lobpcg", "amg"],
        "affinity": ["nearest_neighbors", "rbf"],
        "n_init": randint(10, 21),
        "assign_labels": ["kmeans", "discretize"],
    },
}


def adjust_search_spaces(search_spaces, data):
    max_clusters = len(data) // 3
    for space in search_spaces.values():
        if "n_clusters" in space.keys():
            space["n_clusters"] = (
                Integer(2, max_clusters)
                if isinstance(space["n_clusters"], Integer)
                else randint(2, max_clusters)
            )
    return search_spaces

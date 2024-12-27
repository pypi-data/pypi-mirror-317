import pandas as pd
from clustermatic.bayes_search import BayesSearch
from clustermatic.random_search import RandomizedSearch
from clustermatic.scoring import (
    silhouette_scorer,
    davies_bouldin_scorer,
    calinski_harabasz_scorer,
)
from clustermatic.utils import (
    search_spaces_bayes,
    search_spaces_random,
    adjust_search_spaces,
)
import time


class Optimizer:
    def __init__(
        self,
        optimization_method="bayes",
        n_iterations=30,
        score_metric="silhouette",
        seed=None,
        exclude_algorithms=[],
    ):
        assert optimization_method in [
            "bayes",
            "random",
        ], "Invalid optimization method. Choose from 'bayes' or 'random'."
        self.optimization_method = optimization_method
        self.n_iterations = n_iterations
        self.score_metric = score_metric
        self.scorers = {
            "silhouette": silhouette_scorer,
            "davies_bouldin": davies_bouldin_scorer,
            "calinski_harabasz": calinski_harabasz_scorer,
        }
        assert (
            score_metric in self.scorers
        ), "Invalid score metric. Choose from 'silhouette', 'davies_bouldin', or 'calinski_harabasz'."
        self.scorer = self.scorers[score_metric]
        self.seed = seed
        self.search_spaces = {
            k: v
            for k, v in (
                search_spaces_bayes
                if self.optimization_method == "bayes"
                else search_spaces_random
            ).items()
            if k.__name__ not in exclude_algorithms
        }
        self.scores_ = []
        self.search_class = (
            BayesSearch if self.optimization_method == "bayes" else RandomizedSearch
        )

    def optimize(self, X):
        results = []
        best_models = {}
        search_spaces = (
            adjust_search_spaces(self.search_spaces, X)
            if len(X) < 60
            else self.search_spaces
        )

        for algorithm, param_space in search_spaces.items():
            print(f"Optimizing {algorithm.__name__}")
            search = self.search_class(
                algorithm=algorithm,
                param_space=param_space,
                n_iterations=self.n_iterations,
                scoring_func=self.scorer,
                seed=self.seed,
            )
            start_time = time.time()
            search.fit(X)
            end_time = time.time()
            train_time = end_time - start_time
            self.scores_.append((algorithm.__name__, search.scores_))

            results.append(
                {
                    "Algorithm": algorithm.__name__,
                    "Metric": self.score_metric,
                    "Best Score": search.best_score_,
                    "Best Params": search.best_params_,
                    "Train Time": train_time,
                }
            )

            best_models[algorithm.__name__] = search.best_algorithm_
            print(
                f"{algorithm.__name__} optimized in {train_time:.2f} seconds. Best score: {search.best_score_}"
            )

        sort_ascending = (
            False
            if self.scorer in [silhouette_scorer, calinski_harabasz_scorer]
            else True
        )
        report = (
            pd.DataFrame(results)
            .sort_values(by="Best Score", ascending=sort_ascending)
            .reset_index(drop=True)
        )

        return best_models, report

from sklearn.base import BaseEstimator
from clustermatic.scoring import (
    silhouette_scorer,
    calinski_harabasz_scorer,
    davies_bouldin_scorer,
)
import random


class RandomizedSearch(BaseEstimator):
    def __init__(self, algorithm, n_iterations, param_space, scoring_func, seed=None):
        self.algorithm = algorithm
        self.n_iterations = n_iterations
        self.param_space = param_space
        self.scoring_func = scoring_func
        self.multiplier = (
            -1 if scoring_func in [silhouette_scorer, calinski_harabasz_scorer] else 1
        )
        self.best_score_ = {
            silhouette_scorer: -1,
            davies_bouldin_scorer: 999999,
            calinski_harabasz_scorer: 0,
        }.get(scoring_func, None)
        self.seed = seed
        if self.seed is not None:
            random.seed(self.seed)
        self.scores_ = []

    def fit(self, X):
        def sample_params():
            sampled_params = {}
            for param, space in self.param_space.items():
                if hasattr(space, "rvs"):
                    sampled_params[param] = space.rvs(random_state=self.seed)
                elif isinstance(space, list):
                    sampled_params[param] = random.choice(space)
            return sampled_params

        for _ in range(self.n_iterations):
            param_dict = sample_params()
            model = self.algorithm(**param_dict)

            if hasattr(model, "random_state"):
                model.set_params(random_state=self.seed)

            model.fit(X)
            score = self.scoring_func(model, X)
            self.scores_.append(score)

            if (
                score < self.best_score_ and self.scoring_func == davies_bouldin_scorer
            ) or (
                score > self.best_score_
                and self.scoring_func in [silhouette_scorer, calinski_harabasz_scorer]
            ):
                self.best_score_ = score
                self.best_params_ = param_dict

        if not hasattr(self, "best_params_"):  # FIXME
            self.best_params_ = sample_params()

        self.best_algorithm_ = self.algorithm(**self.best_params_)
        if hasattr(self.best_algorithm_, "random_state"):
            self.best_algorithm_.set_params(random_state=self.seed)

        self.best_algorithm_.fit(X)

        return self

    def predict(self, X):
        assert hasattr(
            self, "best_algorithm_"
        ), "Model not trained. Run fit method before predict."
        return self.best_algorithm_.fit_predict(X)

    def fit_predict(self, X):
        self.fit(X)
        return self.predict(X)

from sklearn.base import BaseEstimator
from skopt import gp_minimize
from clustermatic.scoring import (
    silhouette_scorer,
    calinski_harabasz_scorer,
)


class BayesSearch(BaseEstimator):
    def __init__(self, algorithm, n_iterations, param_space, scoring_func, seed=None):
        self.algorithm = algorithm
        self.n_iterations = n_iterations
        self.param_space = param_space
        self.scoring_func = scoring_func
        self.seed = seed
        self.multiplier = (
            -1 if scoring_func in [silhouette_scorer, calinski_harabasz_scorer] else 1
        )
        self.scores_ = []

    def fit(self, X):
        def objective(params):
            param_dict = {
                key: value for key, value in zip(self.param_space.keys(), params)
            }
            model = self.algorithm(**param_dict)
            model.fit(X)
            score = self.scoring_func(model, X)
            self.scores_.append(score)
            return score * self.multiplier

        result = gp_minimize(
            objective,
            list(self.param_space.values()),
            n_calls=self.n_iterations,
            random_state=self.seed,
        )

        best_params = {
            key: value for key, value in zip(self.param_space.keys(), result.x)
        }

        self.best_algorithm_ = self.algorithm(**best_params)
        self.best_algorithm_.fit(X)
        self.best_score_ = result.fun * self.multiplier
        self.best_params_ = best_params

        return self

    def predict(self, X):
        assert hasattr(
            self, "best_algorithm_"
        ), "Model not trained. Run fit method before predict."
        return self.best_algorithm_.fit_predict(X)

    def fit_predict(self, X):
        self.fit(X)
        return self.predict(X)

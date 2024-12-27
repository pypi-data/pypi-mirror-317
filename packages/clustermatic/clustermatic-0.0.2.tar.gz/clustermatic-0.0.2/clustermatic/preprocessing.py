from sklearn.impute import SimpleImputer
from sklearn.preprocessing import (
    StandardScaler,
    OneHotEncoder,
    MinMaxScaler,
    OrdinalEncoder,
    FunctionTransformer,
)
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer, make_column_selector
from pandas import DataFrame


class Preprocessor:
    def __init__(
        self,
        numerical_impute_strategy="mean",
        categorical_impute_strategy="constant",
        numerical_scaling_strategy="standard",
        categorical_encoding_strategy="onehot",
        reduce_dim=False,
        n_components=2,
    ):
        self.numerical_impute_strategy = numerical_impute_strategy
        self.categorical_impute_strategy = categorical_impute_strategy
        self.categorical_impute_value = "-"

        assert numerical_scaling_strategy in [
            "standard",
            "minmax",
        ], "Invalid numerical scaling strategy"
        self.numerical_scaler = (
            StandardScaler()
            if numerical_scaling_strategy == "standard"
            else MinMaxScaler()
        )

        assert categorical_encoding_strategy in [
            "onehot",
            "ordinal",
        ], "Invalid categorical encoding strategy"
        self.categorical_encoder = (
            OneHotEncoder(handle_unknown="ignore")
            if categorical_encoding_strategy == "onehot"
            else OrdinalEncoder()
        )

        self.reduce_dim = reduce_dim
        self.n_components = n_components

    def process(self, data):
        if not isinstance(data, DataFrame):
            data = DataFrame(data)

        numerical_transformer = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy=self.numerical_impute_strategy)),
                ("scaler", self.numerical_scaler),
            ]
        )

        categorical_transformer = Pipeline(
            steps=[
                (
                    "imputer",
                    SimpleImputer(
                        strategy=self.categorical_impute_strategy,
                        fill_value=self.categorical_impute_value,
                    ),
                ),
                ("encoder", self.categorical_encoder),
            ]
        )

        boolean_transformer = Pipeline(
            steps=[
                (
                    "to_numeric",
                    FunctionTransformer(lambda b: b.astype(int)),
                ),
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("encoder", OrdinalEncoder()),
            ]
        )

        preprocessor = ColumnTransformer(
            transformers=[
                (
                    "num",
                    numerical_transformer,
                    make_column_selector(dtype_include=["int64", "float64"]),
                ),
                (
                    "cat",
                    categorical_transformer,
                    make_column_selector(dtype_include=["object"]),
                ),
                (
                    "bool",
                    boolean_transformer,
                    make_column_selector(dtype_include=["bool"]),
                ),
            ]
        )

        if self.reduce_dim:
            preprocessor_pipeline = Pipeline(
                steps=[
                    ("preprocessor", preprocessor),
                    ("dim_reduction", PCA(n_components=self.n_components)),
                ]
            )
        else:
            preprocessor_pipeline = Pipeline(steps=[("preprocessor", preprocessor)])

        return preprocessor_pipeline.fit_transform(data)

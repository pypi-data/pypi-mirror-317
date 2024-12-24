from typing import List

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


# Temporal elapsed time transformer
class TemporalVariableTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, variables: List[str], reference_variable: str):
        if not isinstance(variables, list):
            raise ValueError('variables should be a list')

        self.variables = variables
        self.reference_variable = reference_variable

    # Fit the Sklearn pipeline
    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        return self

    # Overwrite the original dataframe
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()

        for feature in self.variables:
            X[feature] = X[self.reference_variable] - X[feature]

        return X


# Categorical variable mapper
class Mapper(BaseEstimator, TransformerMixin):
    def __init__(self, variables: List[str], mappings: dict):
        if not isinstance(variables, list):
            raise ValueError('variables should be a list')

        self.variables = variables
        self.mappings = mappings

    # Accomodate the Sklearn pipeline
    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        return self

    # Overwrite the original dataframe
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()

        for feature in self.variables:
            X[feature] = X[feature].map(self.mappings)

        return X

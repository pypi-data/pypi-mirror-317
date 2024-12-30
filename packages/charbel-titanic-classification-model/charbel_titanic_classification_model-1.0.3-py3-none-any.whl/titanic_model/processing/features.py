import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from typing import List
from titanic_model.config.core import config
from sklearn.pipeline import Pipeline

# LETTER TRANSFORMER
class ExtractLetterTransformer(BaseEstimator, TransformerMixin):
    # Extract First Letter of given Variable
    def __init__(self, variables):

        if not isinstance(variables, List):
            raise ValueError("Variables should be a list")
        
        self.variables = variables

    def fit(self, X, y=None):
        # this is only needed for compatibility with sklearn
        return self

    def transform(self, X):

        X = X.copy()

        for feature in self.variables:
            X[feature] = X[feature].str[0]
        
        return X


# CATEGORICAL MISSING IMPUTER
class MyCategoricalImputer(BaseEstimator, TransformerMixin):
    # Impute missing categorical values with 'Missing'
    def __init__(self, variables):
        if not isinstance(variables, List):
            raise ValueError("Variables should be a list")

        self.variables = variables
    
    def fit(self, X, y=None):
        # this is only needed for compatibility with sklearn
        return self
    
    def transform(self, X):

        X = X.copy()

        for feature in self.variables:
            X[feature].fillna('Missing', inplace = True)
        
        return X


# MISSING INDICATOR
class MyAddMissingIndicator (BaseEstimator, TransformerMixin):
    # Add missing indicator for row if we have it in that row
    def __init__ (self,variables):
        if not isinstance(variables, List):
            raise ValueError("Variables should be a list")

        self.variables = variables

    def fit(self, X, y = None):
        # this is only needed for compatibility with sklearn
        return self

    def transform(self, X):

        X = X.copy()

        for feature in self.variables:
            if X[feature].isnull().sum() > 0:
                X[f'{feature}_na'] = X[feature].isnull().astype(int)

        return X

#  MEDIAN IMPUTER
class MyMedianImputer(BaseEstimator, TransformerMixin):
    def __init__(self, variables):
        if not isinstance(variables, List):
            raise ValueError("Variables should be a list")
        self.variables = variables
        self.imputer = SimpleImputer(strategy='median')

    def fit(self, X, y=None):
        self.imputer.fit(X[self.variables])
        return self

    def transform(self, X):
        X = X.copy()
        X[self.variables] = self.imputer.transform(X[self.variables])
        return X
# RARE LABEL ENCODER
class RareLabelCategoricalEncoder(BaseEstimator, TransformerMixin):
    """Groups infrequent categories into a single string"""

    def __init__(self, variables, tol=0.05):

        if not isinstance(variables, list):
            raise ValueError('variables should be a list')
        
        self.tol = tol
        self.variables = variables

    def fit(self, X, y=None):
        # persist frequent labels in dictionary
        self.encoder_dict_ = {}

        for var in self.variables:
            # the encoder will learn the most frequent categories
            t = pd.Series(X[var].value_counts(normalize=True)) 
            # frequent labels:
            self.encoder_dict_[var] = list(t[t >= self.tol].index)

        return self

    def transform(self, X):
        X = X.copy()
        for feature in self.variables:
            X[feature] = np.where(
                X[feature].isin(self.encoder_dict_[feature]),
                                X[feature], "Rare")

        return X

# ONE HOT TRANSFORMER
one_hot_transformer  = Pipeline([
    ('one_hot', OneHotEncoder(drop='first'))
])

one_hot_processor = ColumnTransformer(
    transformers=[('one_hot',one_hot_transformer,config.model_config.categorical_variables)],
    remainder='passthrough'
)





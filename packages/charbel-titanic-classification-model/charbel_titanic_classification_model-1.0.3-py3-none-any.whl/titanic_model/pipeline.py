from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
# from feature_engine.imputation import AddMissingIndicator

from titanic_model.processing.features import one_hot_processor, MyCategoricalImputer, MyAddMissingIndicator, MyMedianImputer, ExtractLetterTransformer, RareLabelCategoricalEncoder
from titanic_model.config.core import config

titanic_pipeline = Pipeline([
    ('cat_imputer', MyCategoricalImputer(variables=config.model_config.categorical_variables)),
    # (
    #         "missing_indicator",
    #         AddMissingIndicator(variables=config.model_config.numerical_variables),
    #     ),
    #('missing_indic', MyAddMissingIndicator(variables=config.model_config.numerical_variables)),
    ('median_imputer', MyMedianImputer(variables=config.model_config.numerical_variables)),
    ('letter_extraction', ExtractLetterTransformer(variables=config.model_config.cabin_variables)),
    ('rare_label_encoder', RareLabelCategoricalEncoder(variables=config.model_config.categorical_variables, tol=0.05)),
    ('preprocessor', one_hot_processor),
    ('scaler', StandardScaler()),
    ('logsitic', LogisticRegression(C=0.0005, random_state=config.model_config.random_state))
])


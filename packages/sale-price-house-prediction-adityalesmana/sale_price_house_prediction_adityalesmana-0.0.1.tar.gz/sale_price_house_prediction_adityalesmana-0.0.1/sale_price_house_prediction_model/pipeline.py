from config.core import config
from feature_engine.encoding import OrdinalEncoder, RareLabelEncoder
from feature_engine.imputation import AddMissingIndicator, CategoricalImputer, MeanMedianImputer
from feature_engine.selection import DropFeatures
from feature_engine.transformation import LogTransformer
from feature_engine.wrappers import SklearnTransformerWrapper
from sklearn.linear_model import Lasso
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Binarizer, MinMaxScaler

from sale_price_house_prediction_model.processing import features as pp

price_pipe = Pipeline(
    [
        # impute categorical variables with string missing
        (
            'missing_imputation',
            CategoricalImputer(
                imputation_method='missing',
                variables=config.model_cnf.categorical_vars_with_na_missing
            )
        ),
        (
            'frequent_imputation',
            CategoricalImputer(
                imputation_method='frequent',
                variables=config.model_cnf.categorical_vars_with_na_frequent
            )
        ),

        # Add Missing Indicator
        (
            'missing_indicator',
            AddMissingIndicator(
                variables=config.model_cnf.numerical_vars_with_na
            )
        ),

        # Impute numerical variables with the mean
        (
            'mean_imputation',
            MeanMedianImputer(
                imputation_method='mean',
                variables=config.model_cnf.numerical_vars_with_na
            )
        ),

        # Temporal variables
        (
            'elapsed_time',
            pp.TemporalVariableTransformer(
                variables=config.model_cnf.temporal_vars,
                reference_variable=config.model_cnf.ref_var
            )
        ),
        (
            'drop_features',
            DropFeatures(
                features_to_drop=[config.model_cnf.ref_var]
            )
        ),

        # Variable Transformation
        (
            'log',
            LogTransformer(
                variables=config.model_cnf.numericals_log_vars
            )
        ),
        (
            'binarizer',
            SklearnTransformerWrapper(
                transformer=Binarizer(threshold=0),
                variables=config.model_cnf.binarize_vars
            )
        ),

        # Mappers
        (
            'mapper_qual',
            pp.Mapper(
                variables=config.model_cnf.qual_vars,
                mappings=config.model_cnf.qual_mappings
            )
        ),
        (
            'mapper_exposure',
            pp.Mapper(
                variables=config.model_cnf.exposure_vars,
                mappings=config.model_cnf.exposure_mappings
            )
        ),
        (
            'mapper_finish',
            pp.Mapper(
                variables=config.model_cnf.finish_vars,
                mappings=config.model_cnf.finish_mappings
            )
        ),
        (
            'mapper_garage',
            pp.Mapper(
                variables=config.model_cnf.garage_vars,
                mappings=config.model_cnf.garage_mappings
            )
        ),

        # Categorical Encoding
        (
            'rare_label_encoder',
            RareLabelEncoder(
                tol=0.01,
                n_categories=1,
                variables=config.model_cnf.categorical_vars
            )
        ),

        # Encode categorical variables using the target mean
        (
            'categorical_encoder',
            OrdinalEncoder(
                encoding_method='ordered',
                variables=config.model_cnf.categorical_vars
            )
        ),
        (
            'scaler',
            MinMaxScaler()
        ),
        (
            'Lasso',
            Lasso(
                alpha=config.model_cnf.alpha,
                random_state=config.model_cnf.random_state
            )
        )
    ]
)

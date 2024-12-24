from sale_price_house_prediction_model.config.core import config
from sale_price_house_prediction_model.processing.features import TemporalVariableTransformer


def test_temporal_variable_transformer(sample_input_data):
    transformer = TemporalVariableTransformer(
        variables=config.model_cnf.temporal_vars,
        reference_variable=config.model_cnf.ref_var
    )
    assert sample_input_data['YearRemodAdd'].iat[0] == 1961

    subject = transformer.fit_transform(sample_input_data)
    assert subject['YearRemodAdd'].iat[0] == 49

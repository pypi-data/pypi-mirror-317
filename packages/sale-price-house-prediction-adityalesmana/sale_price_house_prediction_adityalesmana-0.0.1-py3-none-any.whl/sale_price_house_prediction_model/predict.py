from typing import Any, Dict, Union

import numpy as np
import pandas as pd

from sale_price_house_prediction_model import __version__ as _version
from sale_price_house_prediction_model.config.core import config
from sale_price_house_prediction_model.processing.data_manager import load_pipeline
from sale_price_house_prediction_model.processing.validation import validate_input

pipeline_file_name = f'{config.app_cnf.pipeline_save_file}{_version}.pkl'
_price_pipe = load_pipeline(file_name=pipeline_file_name)


# Make prediction using a saved model pipeline
def make_prediction(*, input_data: Union[pd.DataFrame, Dict[str, Any]]) -> Dict[str, Any]:
    if isinstance(input_data, dict):
        data = pd.DataFrame([input_data])
    else:
        data = input_data

    validated_data, errors = validate_input(input_data=data)
    results: Dict[str, Any] = {
        'predictions': None,
        'version': _version,
        'errors': errors
    }

    if not errors:
        predictions = _price_pipe.predict(X=validated_data[config.model_cnf.features])
        results['predictions'] = [(np.exp(pred)) for pred in predictions]

    return results

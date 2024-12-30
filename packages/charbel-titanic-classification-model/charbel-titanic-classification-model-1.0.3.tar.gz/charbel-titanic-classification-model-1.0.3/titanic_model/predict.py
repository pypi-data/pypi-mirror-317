import typing as t

import pandas as pd

from titanic_model import __version__ as _version
from titanic_model.config.core import config
from titanic_model.processing.data_manager import load_pipeline
from titanic_model.processing.validation import validate_inputs

pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
_titanic_pipe = load_pipeline(file_name=pipeline_file_name)


def make_prediction(
    *,
    input_data: t.Union[pd.DataFrame, dict],
) -> dict:
    """Make a prediction using a saved model pipeline."""

    data = pd.DataFrame(input_data)
    validated_data, errors = validate_inputs(input_data=data)
    results = {"predictions": None, "version": _version, "errors": errors}

    if not errors:
        predictions = _titanic_pipe.predict(
            X=validated_data[config.model_config.features]
        )
        results = {
            "predictions": predictions,
            "version": _version,
            "errors": errors,
        }

    return results


if __name__ == "__main__":
    sample_input_data = {
    "pclass": [3, 1, 2],
    "name": ["Mr. Owen Harris", "Mrs. John Bradley (Florence Briggs Thayer)", "Miss. Laina"],
    "sex": ["male", "female", "female"],
    "age": [22, 38, 26],
    "sibsp": [1, 1, 0],
    "parch": [0, 0, 0],
    "ticket": ["A/5 21171", "PC 17599", "STON/O2. 3101282"],
    "fare": [7.25, 71.2833, 7.925],
    "cabin": [None, "C85", "C123"],
    "embarked": ["S", "C", "S"],
    "boat": [None, 11, None],
    "body": [None, None, None],
    "home.dest": ["St Louis, MO", "Chesterville, ON", "Chesterville, ON"],
    # "title": ["Mr", "Mrs", "Miss"],
    # Add any additional columns needed for your model
    }

    # Convert dictionary to DataFrame
    sample_input_df = pd.DataFrame(sample_input_data)

    # Call make_prediction function
    results = make_prediction(input_data=sample_input_df)

    # Print the results
    print(f"Predictions: {results['predictions']}")
    print(f"Version: {results['version']}")
    print(f"Errors: {results['errors']}")

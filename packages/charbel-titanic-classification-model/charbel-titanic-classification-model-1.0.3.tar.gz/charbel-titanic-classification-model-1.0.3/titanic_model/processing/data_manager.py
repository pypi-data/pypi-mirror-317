
import logging
import typing as t
from pathlib import Path
from typing import Any, Union, List

import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
import numpy as np

import re
from titanic_model import __version__ as _version
from titanic_model.config.core import DATASET_DIR, config, TRAINED_MODEL_DIR

logger = logging.getLogger(__name__)

# processing after directly loading 
def get_first_cabin(row: Any) -> Union[str, float]:
    try:
        return row.split()[0]
    except AttributeError:
        return np.nan

def get_title(passenger: str) -> str:
    """ Extracting passenger title from the name """
    line = passenger
    if re.search('Mrs', line):
        return 'Mrs'
    elif re.search('Mr', line):
        return 'Mr'
    elif re.search('Miss', line):
        return 'Miss'
    elif re.search('Master', line):
        return 'Master'
    else:
        return 'Other'

def pre_loading_pipeline(*, dataframe:pd.DataFrame) -> pd.DataFrame:
    # Replace all ? with np.nan 
    data = dataframe.replace('?', np.nan)

    # get first character of 'cabin' variable
    data['cabin'] = data['cabin'].apply(get_first_cabin)

    # get title from the name variable
    data['title'] = data['name'].apply(get_title)

    # cast 'fare' and 'age' as floats
    data['age'] = data['age'].astype('float')
    data['fare'] = data['fare'].astype('float')

    # drop unnecessary variables
    columns_to_drop = ['name', 'ticket', 'boat', 'body', 'home.dest']
    existing_columns = [col for col in columns_to_drop if col in data.columns]
    data.drop(labels=existing_columns, axis=1, inplace=True)


    return data


def _load_raw_dataset(*, file_name: str) -> pd.DataFrame:
    dataframe = pd.read_csv(Path(f"{DATASET_DIR}/{file_name}"))
    return dataframe

def load_dataset(*, file_name: str) -> pd.DataFrame:
    dataframe = pd.read_csv(Path(f"{DATASET_DIR}/{file_name}"))
    df = pre_loading_pipeline(dataframe=dataframe)

    return df

def save_pipeline(*, pipeline_to_persist: Pipeline) -> None:
    """Persist the pipeline.
    Saves the versioned model, and overwrites any previous
    saved models. This ensures that when the package is
    published, there is only one trained model that can be
    called, and we know exactly how it was built.
    """

    # Prepare versioned save file name
    save_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
    save_path = TRAINED_MODEL_DIR / save_file_name

    remove_old_pipelines(files_to_keep=[save_file_name])
    joblib.dump(pipeline_to_persist, save_path)


def load_pipeline(*, file_name: str) -> Pipeline:
    """Load a persisted pipeline."""

    file_path = TRAINED_MODEL_DIR / file_name
    return joblib.load(filename=file_path)


def remove_old_pipelines(*, files_to_keep: List[str]) -> None:
    """
    Remove old model pipelines.
    This is to ensure there is a simple one-to-one
    mapping between the package version and the model
    version to be imported and used by other applications.
    """
    do_not_delete = files_to_keep + ["__init__.py"]
    for model_file in TRAINED_MODEL_DIR.iterdir():
        if model_file.name not in do_not_delete:
            model_file.unlink()
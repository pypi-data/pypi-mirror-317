from sklearn.model_selection import train_test_split

from titanic_model.config.core import config
from titanic_model.pipeline import titanic_pipeline
from titanic_model.processing.data_manager import load_dataset, save_pipeline


def run_training() -> None:
    """
    Train the model.

    Training data can be found here:
    https://www.openml.org/data/get_csv/16826755/phpMYEkMl
    """


    data = load_dataset(file_name=config.app_config.raw_data_file)

    X_train, X_test, y_train, y_test = train_test_split(
        data[config.model_config.features],  
        data[config.model_config.target],
        test_size=config.model_config.test_size,
        random_state=config.model_config.random_state,
    )

    titanic_pipeline.fit(X_train, y_train)

    save_pipeline(pipeline_to_persist=titanic_pipeline)


if __name__ == "__main__":
    run_training()
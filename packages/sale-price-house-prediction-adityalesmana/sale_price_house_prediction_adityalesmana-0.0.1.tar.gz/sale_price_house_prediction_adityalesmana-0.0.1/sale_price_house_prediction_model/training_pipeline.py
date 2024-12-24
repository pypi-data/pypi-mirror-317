import numpy as np
from config.core import config
from pipeline import price_pipe
from processing.data_manager import load_dataset, save_pipeline
from sklearn.model_selection import train_test_split


# Train the model
def run_training() -> None:
    # read training data
    data = load_dataset(file_name=config.app_cnf.training_data_file)

    # divide train and test set
    X_train, X_test, y_train, y_test = train_test_split(
        data[config.model_cnf.features],
        data[config.model_cnf.target],
        test_size=config.model_cnf.test_size,
        random_state=config.model_cnf.random_state
    )
    y_train = np.log(y_train)

    # fit model
    price_pipe.fit(X_train, y_train)

    # persist trained model
    save_pipeline(pipeline_to_persist=price_pipe)


if __name__ == '__main__':
    run_training()

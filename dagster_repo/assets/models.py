import dagster_repo.assets.config as configs

from dagster import AssetExecutionContext, asset, multi_asset, AssetOut, MetadataValue, Output, StaticPartitionsDefinition
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

import pandas as pd
import numpy as np

GROUP_NAME = 'train_eval_models'

MODELS_MAPPING = {
    'logistic_regression': LogisticRegression,
    'random_forest': RandomForestClassifier
}

PARTITIONS_MODELS = StaticPartitionsDefinition(list(MODELS_MAPPING.keys()))

@multi_asset(
    name='split_dataset',
    description='Split dataset into train and test sets',
    group_name=GROUP_NAME,
    outs={
        'X_train': AssetOut(),
        'X_test':  AssetOut(),
        'y_train': AssetOut(),
        'y_test': AssetOut()
    }
)
def split_dataset(context: AssetExecutionContext, config: configs.SplitDataset, feature_dataset: pd.DataFrame):
    from sklearn.model_selection import train_test_split

    X = feature_dataset['x']
    y = feature_dataset['y']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)

    X_train = X_train.values.reshape(-1, 1)
    X_test = X_test.values.reshape(-1, 1)
    return X_train, X_test, y_train, y_test

@asset(
    name='model',
    description='Train a model',
    group_name=GROUP_NAME,
    partitions_def=PARTITIONS_MODELS
)
def train_model(context: AssetExecutionContext, config: configs.ModelTraining, X_train: np.ndarray, y_train: pd.Series):
    model_name = context.partition_key
    model_params = getattr(config, model_name)
    model = MODELS_MAPPING[model_name](**model_params._convert_to_config_dictionary())
    model.fit(X_train, y_train)

    return Output(
        model
    )

@asset(
    name='evaluate_model',
    description='Evaluate a model',
    group_name=GROUP_NAME,
    partitions_def=PARTITIONS_MODELS
)
def evaluate_model(context: AssetExecutionContext, config: configs.EvaluateModel, X_test: np.ndarray, y_test: pd.Series, model):
    from sklearn.metrics import classification_report
    from sklearn.model_selection import cross_val_score
    import mlflow
    mlflow.set_experiment(config.experiment_name)
    with mlflow.start_run():
        mlflow.sklearn.autolog()
        params = model.get_params()
        mlflow.log_params(params)
        predictions = model.predict(X_test)
        mlflow.log_metric('accuracy', cross_val_score(model,
                                                      X_test,
                                                      y_test,
                                                      cv=config.cv,
                                                      scoring=config.scoring).mean()
                                                      )
    return Output(
        model,
        metadata={
            'classification_report': MetadataValue.json(classification_report(y_test, predictions)),
        }
    )

from dagster import Config


class LoadCsv(Config):
    csv_path: str = 'challenge_edMachina.csv'


class SplitDataset(Config):
    test_size: float = 0.3
    random_state: int = 42


class RandomForestClassifier(Config):
    n_estimators: int = 100
    max_depth: int = 10
    random_state: int = 101


class LogisticRegression(Config):
    random_state: int = 42


class ModelTraining(Config):
    logistic_regression: LogisticRegression
    random_forest: RandomForestClassifier


class EvaluateModel(Config):
    experiment_name: str = 'default'
    cv: int = 5
    scoring: str = 'accuracy'

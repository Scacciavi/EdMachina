from dagster import Config


class LoadCsvConfig(Config):
    csv_path: str = 'challenge_edMachina.csv'

from dagster_repo.assets.config import LoadCsvConfig

from dagstermill import define_dagstermill_asset
from dagster import AssetExecutionContext, asset, file_relative_path, MetadataValue, Output, AssetIn
import pandas as pd

GROUP_NAME = 'download_and_transform_data'

@asset(
    name='raw_student_data',
    description='Materialize a pandas Data',
    group_name=GROUP_NAME,
    io_manager_key='fs_io_manager'
)
def raw_student_data(context: AssetExecutionContext, config: LoadCsvConfig): 
    df = pd.read_csv(config.csv_path, sep=';')
    return Output(
        df,
        metadata={
            'num_rows': len(df),
            'columns': MetadataValue.json(list(df.columns)),
            'csv_path': config.csv_path,
            'preview': MetadataValue.md(df.head().to_markdown())
        }
    )


jupyter_eda_notebook = define_dagstermill_asset(
    name='raw_data_basic_eda',
    notebook_path=file_relative_path(__file__, "../notebooks/basic_eda.ipynb"),
    group_name=GROUP_NAME,
    io_manager_key='output_notebook_io_manager',
    ins={'raw_data': AssetIn('raw_student_data')}
)
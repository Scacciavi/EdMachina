import dagster_repo.assets.config as configs

from dagstermill import define_dagstermill_asset
from dagster import AssetExecutionContext, asset, file_relative_path, MetadataValue, Output, AssetIn
import pandas as pd

GROUP_NAME = 'data_processing'


@asset(
    name='raw_student_data',
    description='Materialize a pandas Data',
    group_name=GROUP_NAME,
    io_manager_key='fs_io_manager'
)
def raw_student_data(context: AssetExecutionContext, config: configs.LoadCsv):
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


@asset(
    name='feature_dataset',
    description='Materialize dataset for model training and evaluation',
    group_name=GROUP_NAME,
    io_manager_key='fs_io_manager'
)
def create_dataset(context: AssetExecutionContext, raw_student_data: pd.DataFrame):
    base_columns = ['periodo', 'user_uuid', 'course_uuid']
    examns_columns = base_columns + ['fecha_mesa_epoch', 'nombre_examen', 'nota_parcial']

    final_grade = raw_student_data.copy()[base_columns + ['nota_final_materia']].drop_duplicates()
    final_grade.rename(columns={'nota_final_materia': 'y'}, inplace=True)

    examns_df = raw_student_data.copy()[examns_columns]
    examns_df.dropna(inplace=True)
    pivot = pd.pivot_table(examns_df, index=['user_uuid', 'course_uuid', 'periodo'], columns='nombre_examen', values='nota_parcial', fill_value=0).reset_index(drop=False)
    pivot['x'] = pivot.apply(lambda x:  x['RECUPERATORIO PRIMER PARCIAL(20)'] if x['RECUPERATORIO PRIMER PARCIAL(20)'] > 0 else x['PRIMER PARCIAL(20)'], axis=1)

    dataset = pd.merge(pivot[base_columns + ['x']], final_grade, on=['user_uuid', 'course_uuid', 'periodo'])

    return Output(
        dataset,
        metadata={
            'num_rows': len(dataset),
            'columns': MetadataValue.json(list(dataset.columns)),
            'preview': MetadataValue.md(dataset.head().to_markdown())
        }
    )

jupyter_eda_notebook = define_dagstermill_asset(
    name='raw_data_basic_eda',
    notebook_path=file_relative_path(__file__, "../notebooks/basic_eda.ipynb"),
    group_name=GROUP_NAME,
    io_manager_key='output_notebook_io_manager',
    ins={'raw_data': AssetIn('raw_student_data')}
)
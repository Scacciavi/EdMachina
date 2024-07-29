from dagster import Definitions, load_assets_from_modules, FilesystemIOManager
from dagstermill import ConfigurableLocalOutputNotebookIOManager

from dagster_repo.assets import data_load

all_assets = load_assets_from_modules([data_load])

defs = Definitions(
    assets=all_assets,
    resources={
        "output_notebook_io_manager": ConfigurableLocalOutputNotebookIOManager(),
        "fs_io_manager": FilesystemIOManager(),
    }
)

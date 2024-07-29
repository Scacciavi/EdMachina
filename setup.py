import setuptools
import os

DAGSTER_VERSION = os.getenv('DAGSTER_VERSION', '1.7.9')
DAGSTER_LIBS_VERSION = os.getenv('DAGSTER_LIBS_VERSION', '0.23.9')
MLFLOW_VERSION = os.getenv('MLFLOW_VERSION', '2.15.0')

setuptools.setup(
    name="edmachina-ml-challenge",
    packages=setuptools.find_packages(),
    install_requires=[
        f"dagster=={DAGSTER_VERSION}",
        f"dagster-webserver=={DAGSTER_VERSION}",
        f" mlflow=={MLFLOW_VERSION}",
        "pandas==2.2.2"
    ],
    extras_require={"dev": [
        f"dagster-webserver=={DAGSTER_VERSION}",
        f"dagstermill=={DAGSTER_LIBS_VERSION}",
        "jupyter",
        "pytest"
    ]}

)

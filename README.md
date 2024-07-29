# EdMachina

## Local Dev configuration
1. Create the environment
```sh
	conda env create --file conda.yaml
    conda activate edmachina-ml-challenge
```
2. Install dependencies
```sh
	set -o allexport; source environments/local.env; set +o allexport 
    pip install --editable .
```



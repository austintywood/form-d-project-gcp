# Form D Data Engineer Project
## Summary
This project showcases the ability to design and deploy data engineering solutions and practices, including:
- ETL & ELT Pipelines
- Workflow Orchestration
- Data Lakes
- Data Warehouses
- Data Visualizations

This project contains everything necessary to setup the required resources for running this pipeline on your own!

## Setup
_This project was developed using Python 3.10. Support for other versions of Python is not guaranteed_

1. Clone this project codebase.

2. Set up virtual python environment.
```powershell
# Note that the `python` executable for your installation of Python 3.10 may differ on Unix, Bash
# Ensure virtualenv
python -m pip install virtualenv

# Create venv
python -m venv .venv

# Activate venv
.venv/scripts/activate      # Windows, Powershell
source .venv/bin/activate   # Unix, Bash

# Install requirements
python -m pip install -r requirements.txt
```

3. Set up Google Cloud Platform Service Account Credentials.
    1. Create a new project in GCP
    2. With your new project selected, navigate to APIs & Services -> Credentials
    3. Create Credentials -> Service Account
        - Default permissions should be sufficient ("Owner")
    4. Open the Service Account -> Keys -> Add Key -> Create Key (JSON)
    5. Download the .json credentials file to `/path/to/project/.gcp/creds.json`

4. Populate `.env` file and set up GCP resources, including:
    - Google Cloud Storage Bucket _(data lake)_
        - _Make sure to adhere to bucket naming constraints_
    - Google BigQuery Dataset _(data warehouse, landing)_
        - _`raw` dataset is created during this step. `form_d` dataset is created later by dbt._
```powershell
# Run setup script
python setup.py --bucket <BUCKET-NAME>
```

5. Execute the following two scripts to perform the following steps.
    1. Get Form D data files (.tsv) made publically available by the SEC and store them in Google Cloud Storage.
    2. Read the data from these Form D data files and write them to staging/landing tables in Google BigQuery.
```powershell
# Ingest SEC Form D .tsv files to Google Cloud Storage bucket (data lake)
python scripts/sec_to_gcs.py

# Load the data lake to Google BigQuery (data warehouse, landing)
python scripts/gcs_to_bq.py
```

6. Due to project structure, set the following environment variables for easy dbt execution:
```bash
# Unix, Bash
export DBT_PROFILES_DIR=$(pwd)/dbt_form_d
export DBT_PROJECT_DIR=$(pwd)/dbt_form_d
```
```powershell
# Windows, Powershell
$env:DBT_PROFILES_DIR=(Get-Location).path + "\dbt_form_d"
$env:DBT_PROJECT_DIR=(Get-Location).path + "\dbt_form_d"
```

7. Run the dbt pipeline
```powershell
dbt run
```
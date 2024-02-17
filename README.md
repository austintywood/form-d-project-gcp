```powershell
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

1. Create a new project in GCP
2. With your new project selected, navigate to APIs & Services -> Credentials
3. Create Credentials -> Service Account
    - Default permissions should be sufficient ("Owner")
4. Open the Service Account -> Keys -> Add Key -> Create Key (JSON)
5. Download the .json credentials file to `/path/to/project/.gcp/creds.json`

```powershell
# Run setup script
python setup.py --bucket <BUCKET-NAME> --dataset <DATASET_NAME>
```
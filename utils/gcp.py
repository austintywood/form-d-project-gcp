import dotenv
dotenv.load_dotenv()
import os
from google.cloud import storage as gcs

# Specify credentials file and ensure it exists
def set_gcp_creds(root_dir: str | None = None):
    """Set GCP credentials; ensure existence of creds file"""
    if root_dir != None:
        creds_file = os.path.join(root_dir, '.gcp', 'creds.json')
    else:
        creds_file = os.path.join(os.getenv('ROOT_DIR'), '.gcp', 'creds.json')
    open(creds_file, 'r')
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds_file

    return creds_file

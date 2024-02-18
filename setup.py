import os
import site
import sys
import utils.gcp
from google.cloud import storage as gcs
from google.cloud import bigquery as bq
from google.cloud.exceptions import NotFound
from google.api_core.exceptions import Forbidden
import argparse
import json
import logging
from textwrap import dedent


def parse_args():
    parser = argparse.ArgumentParser(description='Setup GCP resources and environment')
    parser.add_argument('--bucket', type=str, required=True, help='Name of the GCS bucket')
    return parser.parse_args()

def add_dotenv(key, val):
    env_file = os.path.join(os.path.dirname(sys.prefix), '.env')

    if not os.path.exists(env_file):
        with open(env_file, 'w') as f:
            f.write(f"{key}={val}\n")
    else:
        with open(env_file, 'r') as f:
            lines = f.readlines()

        key_exists = False
        for i, l in enumerate(lines):
            if l.startswith(f"{key}="):
                key_exists = True
                lines[i] = f"{key}={val}\n"
                break
        if not key_exists:
            lines.append(f"{key}={val}\n")

        with open(env_file, 'w') as f:
            f.writelines(lines)

def setup_root_dir():
    """Verify the pathing for necessary .pth and .env files"""

    # Create root_dir.pth file
    root_dir_pth = os.path.join(site.getsitepackages()[-1], 'root_dir.pth')
    root_dir = os.path.dirname(sys.prefix)
    with open(root_dir_pth, 'w') as f:
        f.write(root_dir)

    # Add the ROOT_DIR environment variable to .env file
    add_dotenv('ROOT_DIR', root_dir)

    return root_dir

def setup_gcp_resources(bucket_name: str, root_dir: str):
    """Verify and set up the required GCP resources"""

    # Set GCP credentials for the following steps
    utils.gcp.set_gcp_creds(root_dir)

    # Google Cloud Storage Bucket
    gcs_client = gcs.Client()
    bucket = gcs_client.bucket(bucket_name)
    try:
        if not bucket.exists():
            bucket.create(predefined_acl='private')
    except Forbidden:
        bucket.create(predefined_acl='private')
    add_dotenv('BUCKET_NAME', bucket_name)

    # Google BigQuery Dataset
    bq_client = bq.Client()
    dataset_name = 'raw'
    dataset = bq_client.dataset(dataset_name)
    try:
        bq_client.get_dataset(dataset)
    except NotFound:
        bq_client.create_dataset(dataset)
    add_dotenv('DATASET_NAME', dataset_name)

    return

def setup_dbt_profiles_yml(root_dir):
    """Verify and set up the profiles.yml file within dbt subdirectory"""

    # Get the project_id from gcp creds file
    creds_file = os.path.join(root_dir, '.gcp', 'creds.json')
    with open(creds_file, 'r') as f:
        content: dict = json.load(f)
    project_id = content.get('project_id')


    # Verify the existence of the profiles.yml file
    # Warn & return if not exists
    profiles_yml_file = os.path.join(root_dir, 'dbt_form_d', 'profiles.yml')
    if not os.path.isfile(profiles_yml_file):
        warning = dedent(f"""
            {profiles_yml_file} does not exist.
            Unable to set up dbt at this time.
            Pull git and try again.
        """)
        logging.warning(warning)
        return

    # Populate the keyfile and project values in the profiles.yml file
    with open(profiles_yml_file, 'r') as f:
        lines = f.readlines()

    for i, l in enumerate(lines):
        if l.strip().startswith('keyfile:'):
            lines[i] = f"{l.split(':')[0]}: {creds_file}\n"
        elif l.strip().startswith('project:'):
            lines[i] = f"{l.split(':')[0]}: {project_id}\n"

    with open(profiles_yml_file, 'w') as f:
        f.writelines(lines)

    return

def main():
    args = parse_args()
    root_dir = setup_root_dir()
    setup_gcp_resources(args.bucket, root_dir)
    setup_dbt_profiles_yml(root_dir)

if __name__ == '__main__':
    main()

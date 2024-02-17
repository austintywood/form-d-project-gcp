import os
import site
import sys
import utils.gcp
from google.cloud import storage as gcs
from google.cloud import bigquery as bq
from google.cloud.exceptions import NotFound
from google.api_core.exceptions import Forbidden
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Setup GCP resources and environment')
    parser.add_argument('--bucket', type=str, required=True, help='Name of the GCS bucket')
    parser.add_argument('--dataset', type=str, required=True, help='Name of the BigQuery dataset')
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

def setup_gcp_resources(bucket_name: str, dataset_name: str, root_dir: str):
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
    dataset = bq_client.dataset(dataset_name)
    try:
        bq_client.get_dataset(dataset)
    except NotFound:
        bq_client.create_dataset(dataset)
    add_dotenv('DATASET_NAME', dataset_name)

    return

def main():
    args = parse_args()
    root_dir = setup_root_dir()
    setup_gcp_resources(args.bucket, args.dataset, root_dir)

if __name__ == '__main__':
    main()
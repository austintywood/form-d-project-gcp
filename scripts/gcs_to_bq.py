import dotenv
dotenv.load_dotenv()
import os
import utils.gcp
from google.cloud import storage as gcs
from google.cloud import bigquery as bq
from google.cloud.exceptions import NotFound
import pandas as pd
from io import StringIO
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging


def gcs_tsv_to_bq_table(
    entity: dict,
    bucket_name: str,
    dataset_name: str
):
    """Reads data from .tsv files in GCS buckets; writes to tables in BigQuery

    Parameters
    ----------
    entity : dict
        `{'raw_name': 'clean_name'}`
    bucket_name : str
        Name of gcs bucket, stored in .env file, set using setup.py
    dataset_name: str
        Name of bq dataset, stored in .env file, set using setup.py

    Raises
    ------
    Exception
        Generic Exception if unable to get/create BigQuery table object
    """
    # Initialize the Google Cloud Storage & BigQuery Clients
    gcs_client = gcs.Client()
    bq_client = bq.Client()

    # Initialize the gcs bucket
    bucket = gcs_client.bucket(bucket_name)

    # Create empty dataframe list to populate (append)
    df_list = []

    # Iterate through bucket objects to identify entity data based on raw_name
    for b in bucket.list_blobs():

        # Get content, create, dataframe and append to df_list
        if b.name.endswith(f"{list(entity.keys())[0]}.tsv"):
            content = b.download_as_string().decode('utf-8')
            df_list.append(
                pd.read_csv(StringIO(content), delimiter='\t', dtype='str')
            )

    # Concatenate dataframes to obtain whole entity dataset
    df = pd.concat(df_list)

    # Create BigQuery tables if they do not already exist
    dataset_ref = bq_client.dataset(dataset_name)
    table_ref = dataset_ref.table(list(entity.values())[0])

    try:
        table = bq_client.get_table('.'.join(
            [bq_client.project, dataset_ref.dataset_id, table_ref.table_id]
        ))
    except NotFound:
        schema = [bq.SchemaField(c, 'STRING') for c in df.columns]
        table = bq.Table(table_ref, schema=schema)
        bq_client.create_table(table)
    except Exception as e:
        raise e

    # Truncate & write to tables
    job_config = bq.LoadJobConfig(write_disposition='WRITE_TRUNCATE')
    bq_client.load_table_from_dataframe(df, table_ref, job_config=job_config)


def main():
    # Set GCP creds
    utils.gcp.set_gcp_creds()

    # Execute threads for each entity
    # Set max_workers to the number of entities
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = [
            executor.submit(
                gcs_tsv_to_bq_table,
                entity,
                os.getenv('BUCKET_NAME'),
                os.getenv('DATASET_NAME'),
            ) for entity in [
                {'FORMDSUBMISSION': 'submissions'},
                {'ISSUERS': 'issuers'},
                {'OFFERING': 'offerings'},
                {'RECIPIENTS': 'recipients'},
                {'RELATEDPERSONS': 'related_persons'},
                {'SIGNATURES': 'signatures'}
            ]
        ]

        # Raise exceptions as identified in futures
        for future in as_completed(futures):
            future.result()


if __name__ == '__main__':
    main()

import dotenv
dotenv.load_dotenv()
import os
import requests
from bs4 import BeautifulSoup
import utils.gcp
from google.cloud import storage as gcs
import pandas as pd
from io import BytesIO
from zipfile import ZipFile
from concurrent.futures import ThreadPoolExecutor, as_completed


# Set vars to be used across functions
SEC_URL = 'https://www.sec.gov'
HEADERS = {'User-Agent': 'Chrome/121.0.0.0'}

def get_new_data_hrefs() -> pd.DataFrame:
    # Retrieve the quarters which are available from SEC
    resp = requests.get(
        url=f"{SEC_URL}/dera/data/form-d",
        headers=HEADERS,
    )
    resp.raise_for_status()

    # From soup, build available data payload for year, quarter, and hrefs
    soup = BeautifulSoup(resp.text, 'html.parser')
    table = soup.find('table')
    data = [
        {
            'year': a.text.split(' ')[0],
            'quarter': a.text.split(' ')[1][-1],
            'href': a.get('href'),
        } for a in table.find_all('a')
    ]

    # Initialize dataframe for easy data merging
    df_sec = pd.DataFrame(data, dtype=str)

    # Retrieve the quarters which already exist in GCP
    gcs_client = gcs.Client()
    bucket = gcs_client.bucket(os.getenv('BUCKET_NAME'))

    # Iterate through blobs and parse out year/quarter
    data = []
    for b in bucket.list_blobs():
        blob_details = {'year': b.name[0:4], 'quarter': b.name[5]}
        if blob_details not in data:
            data.append(blob_details)

    # Initialize dataframe for easy merging
    df_gcp = pd.DataFrame(data, dtype=str)
    if df_gcp.empty:
        df_gcp = pd.DataFrame({c: [] for c in ['year', 'quarter']})

    # Merge the two dataframes, keeping only the newly available data
    df_new = (
        df_sec
        .merge(df_gcp, on=['year', 'quarter'], how='left', indicator=True)
        .query('_merge == "left_only"')
        .drop(columns=['_merge'])
    )

    # Return list of hrefs for newly available data quarters
    new_data_hrefs = [r['href'] for i, r in df_new.iterrows()]

    return new_data_hrefs

def upload_zip_contents_to_gcs(href: str):
    # Obtain response for .zip href
    resp = requests.get(
        url=f"{SEC_URL}{href}",
        headers=HEADERS,
    )
    resp.raise_for_status()

    # Initialize ZipFile object, gcs client, and bucket
    zf = ZipFile(BytesIO(resp.content))
    gcs_client = gcs.Client()
    bucket = gcs_client.bucket(os.getenv('BUCKET_NAME'))

    # Iterate through the zipfile files, clean file names, & upload to gcs
    for n in zf.namelist():
        data = zf.read(n)
        b = n.replace('_d', '').replace('_0', '').replace('Q', 'q')
        blob = bucket.blob(b)
        with BytesIO(data) as f:
            blob.upload_from_file(f, content_type='application/octet-stream')

def main():
    # Set GCP creds
    utils.gcp.set_gcp_creds()

    # Obtain the hrefs for quarterly data not yet existing in the bucket
    hrefs = get_new_data_hrefs()

    # Execute threads for each href
    # Set max_workers at will; more threads can cause TimeoutErrors
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(
                upload_zip_contents_to_gcs
                , href
            ) for href in hrefs
        ]

    # Raise exceptions as identified in futures
    for future in as_completed(futures):
        future.result()

if __name__ == '__main__':
    main()

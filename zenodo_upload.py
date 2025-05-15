import argparse
import os

import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper

HEADERS = {'Content-Type': 'application/json'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upload to Zenodo')
    parser.add_argument('token', type=str, help='Zenodo API token')
    parser.add_argument('deposition', type=str, help='Zenodo deposition ID')
    parser.add_argument('files', nargs='+', default=[], help='File(s) to upload')
    args = parser.parse_args()

    params = {'access_token': args.token}
    with requests.Session() as session:
        retry = Retry(connect=5, backoff_factor=2)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        r = session.get(f'https://zenodo.org/api/deposit/depositions/{args.deposition}', params=params, headers=HEADERS)
        bucket_url = r.json()['links']['bucket']

        for file_path in args.files:
            file_size = os.stat(file_path).st_size
            file_name = os.path.basename(file_path)
            with open(file_path, 'rb') as file:
                with tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024, desc=file_name) as t:
                    wrapped_file = CallbackIOWrapper(t.update, file, 'read')
                    r = session.put(f'{bucket_url}/{file_name}', data=wrapped_file, params=params, timeout=60)
                    r.raise_for_status()

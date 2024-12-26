import time
import requests
import json
import logging
from requests_toolbelt.multipart.encoder import MultipartEncoder
from typing import Dict, Any

# Constants
API_URL = 'https://api.metadefender.com/v4/file'
TIMEOUT = 10  # seconds

# Create a library-specific logger
logger = logging.getLogger('file_scan_dd')

def scan_file(api_key: str, file_path: str, metadata: Dict[str, Any] = {}) -> Dict[str, Any]:
    try:
        with open(file_path, 'rb') as file:
            form = MultipartEncoder(
                fields={
                    'file': ('filename', file),
                    'metadata': (None, json.dumps(metadata), 'application/json')
                }
            )

            response = requests.post(
                API_URL,
                data=form,
                headers={
                    'apikey': api_key,
                    'Content-Type': form.content_type,
                    'samplesharing': '0',
                    'privateprocessing': '1'
                },
                timeout=TIMEOUT
            )

            response.raise_for_status()
            data_id = response.json().get('data_id')
            if not data_id:
                raise ValueError("No data_id returned in response")

            time.sleep(1)  # Wait for the file to be processed
            scan_result = get_scan_result(api_key, data_id)
            if not scan_result['is_clean']:
                return {
                    'status': 422,
                    'error': 'File is infected!'
                }

            return {
                'status': 200,
                'data': scan_result
            }
    except requests.exceptions.RequestException as error:
        logger.error(f"Request failed: {error}")
        if error.response:
            return {
                'status': error.response.status_code,
                'error': error.response.json()
            }
        else:
            return {
                'status': 500,
                'error': str(error)
            }
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return {
            'status': 500,
            'error': str(e)
        }

def get_scan_result(api_key: str, data_id: str, max_retries: int = 20, delay: int = 5) -> Dict[str, Any]:
    try:
        retries = 0
        scan_result = None
        while retries < max_retries:
            response = requests.get(
                f'{API_URL}/{data_id}',
                headers={'apikey': api_key},
                timeout=TIMEOUT
            )
            response.raise_for_status()
            scan_result = response.json()
            progress = scan_result['scan_results']['progress_percentage']
            if progress == 100:
                break
            time.sleep(delay)
            retries += 1
        if retries == max_retries:
            raise TimeoutError('Scan timed out.')
        return {
            'scan_result': scan_result,
            'is_clean': scan_result['scan_results']['scan_all_result_a'] == 'No Threat Detected'
        }
    except requests.exceptions.RequestException as error:
        logger.error(f"Request failed: {error}")
        raise requests.exceptions.RequestException(error.response.json() if error.response else str(error))
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise RuntimeError(str(e))
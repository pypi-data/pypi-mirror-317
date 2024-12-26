# file_scan_dd

A Python library for scanning files using the Metadefender API.

## Installation

```
pip install file_scan_dd
```
## Usage
```
from file_scan_dd import scan_file

api_key = 'your_api_key'
file_path = 'path_to_your_file'
metadata = {}

result = scan_file(api_key, file_path, metadata)
print(result)
```
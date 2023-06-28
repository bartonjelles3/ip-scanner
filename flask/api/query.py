import requests

url = 'http://127.0.0.1:5000/scan'

payload = {
    'ips': ['127.0.0.1:8080'],
    'scan_software': True,
    'scan_root': True,
    'preserve_ips': True,
    'log_level': 'WARNING'
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    print(response.json())
else:
    print(f'Request failed with status code {response.status_code}')
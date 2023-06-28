import requests

# Define the URL of the Flask application
url = 'http://127.0.0.1:5000/scan'

# Prepare the request payload
payload = {
    'ips': ['127.0.0.1:8080'],
    'scan_software': True,
    'scan_root': True,
    'preserve_ips': True,
    'log_level': 'WARNING'
}

# Send the POST request
response = requests.post(url, json=payload)

# Check the response status code
if response.status_code == 200:
    # Print the response content
    print(response.json())
else:
    print(f'Request failed with status code {response.status_code}')

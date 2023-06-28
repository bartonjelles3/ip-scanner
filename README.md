# IP Scanner

A simple but extensible and robust IP scanning tool that checks a list of given IPs (via a CLI wrapper or WIP web UI and JSON API) and returns if a flagged version of NGINX or Microsoft IIS is running (version currently hard-coded to meet project requirements), and if a directory listing is available at root (/).

## Limitations
Only accepts a naked IP plus port, hostname plus potential path would be desirable. If the page tries to re-direct an exception will be raised, meaning the server software may not be able to be checked. This enforces checking of root but may cause issues if server software needs to be checked, regardless of path.

The root directory listing check is rudimentary and only checks if the page contains 'Index of', which is common practice, but not set in stone.

## Installation
Install ip-scanner-project from PyPI with pip.

```bash
  pip install ip-scanner-project
```

## Usage
Run the tool with `ip-scanner-project-cli`. (Only tested on Linux). `--help` shows available parameters, but the key ones are `--ips` and `--ip-file`. `--ips` Expects a space separated list of IPs, `--ip-file` expects a file with an IP on each line.

IPs should be in the following format (parentheses means optional): `(http://)127.0.0.1(:8080)`.

```bash
$ ip-scanner-project-cli --ip-file=/tmp/ips.txt
Running scan.
http://127.0.0.1:8080
Web server software: Unflagged
Root listing: Unavailable

http://127.0.0.2
Web server software: Error occurred while checking this server for web server
Root listing: Error occurred while checking this server for dir listing
Error occurred during scan.
Error name: Failure in response, see logs or status...
Error message: Bad status... HTTPConnectionPool(host='127.0.0.2', port=80): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7f969c9fb050>: Failed to establish a new connection: [Errno 111] Connection refused'))
```

You can also specify JSON output with --output-method. "HUMAN" (default) will only print error messages if applicable but JSON will do it always for consistent output. You can use the enums if you choose to parse the output, available in the repo at scanner/utils.py.

## Local usage and testing
Clone the repo and install the dependencies (requests, termcolor, and requests_mock, requirements.txt incoming). Set $PYTHONPATH as needed. All tests can be ran with `python -m unittest discover -s tests -p '*test.py'`.

## Future work
-Flask web UI and exposed RESTful API with Docker image.

-Ability to pass paths and accept re-directs, and disable root checking when this occurs.

-Ability to change flagged versions (simple but not in project requirements).

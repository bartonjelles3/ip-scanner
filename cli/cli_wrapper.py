import argparse
import sys

from ..scanner import utils
from ..scanner import web_server_scanner

def main():
    parser = argparse.ArgumentParser(description='Checks if provided IPs match '
                                     'server type and version from '
                                     f'{utils.get_flagged_versions()}.'
                                     'Also runs very simple, unreliable '
                                     'check to see if a listing of files is '
                                     ' available at root (ip + /).')
    parser.add_argument('--ips', nargs='+', type=str, help='1 or more IP addresses to scan.')
    parser.add_argument('--disable-scan-software', action='store_false', help='Scan for web server software.')
    parser.add_argument('--disable-scan-root', action='store_false', help='Scan for directory listings at root.')
    parser.add_argument('--preserve-ips', action='store_true', help='Preserve original IPs in output.')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        default='WARNING', help='Set the log level.')
    args = parser.parse_args()
    
    if not args.ips:
        print('IPs must be passed.')
        sys.exit(1)

    print('Running scan.')
    result = web_server_scanner.WebServerScanner(args.ips,
                                                args.disable_scan_software,
                                                args.disable_scan_root,
                                                args.preserve_ips,
                                                args.log_level)()
    _print_output(result)

def _print_output(result: web_server_scanner.IP_MAP_TYPE):
    formatted_result = ''
    for k, v in result.items():
        # Get enum value for each item except for status which is a string.
        sw_type, root_listing, error = (item.value for item in v[:3])
        status = v[3]
        msg = f'{k}: Web server: {sw_type}. Root listing: {root_listing}.'
        error_msg = f'Error occurred: {error}, {status}.' if error != utils.StatusEnum.good else ''
        formatted_result += f'{msg} {error_msg}\n\n'
    print(formatted_result)

if __name__ == '__main__':
    main()
import argparse
import logging

import web_server_scanner
import utils
# Thoughts: Show unflagged vers that have root available? Show root avail with flagged vers?
def main():
    parser = argparse.ArgumentParser(description='Checks if provided IPs match '
                                     'server type and version from '
                                     f'{utils.get_flagged_versions()}.'
                                     'Also runs very simple, unreliable '
                                     'check to see if a listing of files is '
                                     ' available at root (ip + /).')
    parser.add_argument('--ips', nargs='+', help='IP addresses to scan.')
    parser.add_argument('--disable-scan-software', action='store_false', help='Scan for web server software.')
    parser.add_argument('--disable-scan-root', action='store_false', help='Scan for directory listings at root.')
    parser.add_argument('--preserve-ips', action='store_true', help='Preserve original IPs in output.')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        default='WARNING', help='Set the log level.')
    args = parser.parse_args()

    try:
        result = web_server_scanner.WebServerScanner(args.ips,
                                                           args.disable_scan_software,
                                                           args.disable_scan_root,
                                                           args.preserve_ips,
                                                           args.log_level)()
    except ValueError as e:
        print(f'Exception raised. Did you pass IPs? {e}')
        return
    _print_output(result)


def _print_output(result: web_server_scanner.IP_MAP_TYPE):
    msg = ''
    for k, v in result.items():
        sw_type = v[0].value
        root_listing = v[1].value
        msg += f'{k}: {sw_type}, root listing: {root_listing}'
    print(msg)

if __name__ == '__main__':
    main()
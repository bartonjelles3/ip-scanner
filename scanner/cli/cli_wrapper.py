import argparse
import sys
import json
from termcolor import colored as text_color

import utils
import web_server_scanner

def main():
    parser = argparse.ArgumentParser(description='Checks if provided IPs match '
                                     'server type and version from '
                                     f'{utils.get_flagged_versions()}.'
                                     'Also runs very simple, unreliable '
                                     'check to see if a listing of files is '
                                     ' available at root (ip + /).')
    parser.add_argument('--ips', nargs='+', type=str, help='Space separated IP addresses to scan.')
    parser.add_argument('--disable-scan-software', action='store_false', help='Scan for web server software.')
    parser.add_argument('--disable-scan-root', action='store_false', help='Scan for directory listings at root.')
    parser.add_argument('--preserve-ips', action='store_true', help='Preserve original IPs in output.')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        default='CRITICAL', help='Set the log level.')
    parser.add_argument('--output-method', choices=['HUMAN', 'JSON'],
                        default='HUMAN', help='How to print output to console.')
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
    if args.output_method == 'HUMAN':
        _print_human(result)
    if args.output_method == 'JSON':
        _print_json(result)

def _print_human(result: web_server_scanner.IP_MAP_TYPE):
    msg = ''
    for ip, v in result.items():
        # Get enum value for each item except for status which is a string.
        sw_type, root_listing, status = (enum_member.value for enum_member in list(v.values())[:3])
        error_msg = v['ErrorMsg']
        msg += (f'\n\n{text_color(ip, color="cyan", attrs=["bold"])}' 
               f'\n{text_color("Web server software:", attrs=["bold"])} {sw_type}' 
               f'\n{text_color("Root listing:", attrs=["bold"])} {root_listing}')
        if status != utils.StatusEnum.good.value:
            msg += (f'\n{text_color("Error occurred during scan.", color = "red", attrs=["bold"])}'
                    f'\n{text_color("Error name:", color = "red", attrs=["bold"])} {status}'
                    f'\n{text_color("Error message:", color = "red", attrs=["bold"])} {error_msg}')
    print(msg)
    
def _print_json(result: web_server_scanner.IP_MAP_TYPE):
    print(json.dumps(result, indent=4))

if __name__ == '__main__':
    main()
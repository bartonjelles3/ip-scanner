"A CLI wrapper for web_server_scanner, takes IPs and returns flagged servers."
import argparse
import sys
import json
from termcolor import colored as text_color

import utils
import web_server_scanner

def main():
    parser = argparse.ArgumentParser(description='Checks if provided IPs match '
                                     'server type and version from '
                                     f'{utils.get_flagged_versions()}. '
                                     'Also runs a very simple, unreliable '
                                     'check to see if a listing of files is '
                                     'available at root (ip + /).')
    parser.add_argument('--ips', nargs='+', type=str, help='Space separated IP addresses to scan.')
    parser.add_argument('--ip-file', type=str, help='Text file containing IP addresses (one per line).')
    parser.add_argument('--disable-scan-software', action='store_false', help='Disable scan for web server software.')
    parser.add_argument('--disable-scan-root', action='store_false', help='Disable scan for directory listings at root.')
    parser.add_argument('--preserve-ips', action='store_true', help='Preserve original IPs in output.')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        default='CRITICAL', help='Set the log level.')
    parser.add_argument('--output-method', choices=['HUMAN', 'JSON'],
                        default='HUMAN', help='How to print output to console.')
    args = parser.parse_args()
    
    if args.ips and args.ip_file:
        print('Both --ips and --ip-file cannot be provided together.')
        sys.exit(1)

    if args.ips:
        ips = args.ips
    elif args.ip_file:
        ips = _read_ip_file(args.ip_file)
    else:
        print('IPs must be provided using either --ips or --ip-file.')
        sys.exit(1)

    print('Running scan.')
    result = web_server_scanner.WebServerScanner(ips,
                                                args.disable_scan_software,
                                                args.disable_scan_root,
                                                args.preserve_ips,
                                                args.log_level)()
    if args.output_method == 'HUMAN':
        _print_human(result)
    if args.output_method == 'JSON':
        _print_json(result)

def _read_ip_file(file_path: str) -> list[str]:
    try:
        with open(file_path, 'r') as file:
            ips = [line.strip() for line in file.readlines()]
        return ips
    except FileNotFoundError:
        print(f'File not found: {file_path}')
        sys.exit(1)

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
            msg += (f'\n{text_color("Error occurred during scan.", color="red", attrs=["bold"])}'
                    f'\n{text_color("Error name:", color="red", attrs=["bold"])} {status}'
                    f'\n{text_color("Error message:", color="red", attrs=["bold"])} {error_msg}')
    print(msg)
    
def _print_json(result: web_server_scanner.IP_MAP_TYPE):
    print(json.dumps(result, indent=4))

if __name__ == '__main__':
    main()
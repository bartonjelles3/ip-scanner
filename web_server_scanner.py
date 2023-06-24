import requests
import utils
import logging
import os
import re
from typing import Optional

WEBSRVENUM = utils.WebServerSoftwareEnum
WEBSRVVERS = utils.get_flagged_versions()
DIRLISTENUM = utils.DirListingEnum
STATUSENUM = utils.StatusEnum
# Format for mapping IPs to requested info. Last item is for detailed status if error.
IP_MAP_TYPE = dict[str, tuple[WEBSRVENUM, DIRLISTENUM, STATUSENUM, Optional[str]]]

_ERROR_STATUS_MSG = 'Bad status... {}'
_REQUEST_TIMEOUT = 3 # seconds

ip = '127.0.0.1:8080'


class WebServerScanner():
    """Scan web server from list of IPs to check web server type and / dir listing."""
    def __init__(self, ips: list, scan_software: bool = True, scan_root: bool = True,
                 preserve_ips: bool = True, log_level: str = 'WARNING') -> None:
        self.ips = ips
        self.scan_software = scan_software
        self.scan_root = scan_root
        self.preserve_ips = preserve_ips
        self.ip_map: IP_MAP_TYPE = {}
        logging.basicConfig(level=log_level)
        logging.debug(f'WebServerScanner() called with {locals()}.')

    def __call__(self) -> IP_MAP_TYPE:
        """"Iterate over each IP, format, check for issues and status, return dict.
            
            Main logic. If something is wrong where a server cannot be checked
            at all, 3 bad enums will be returned (for consistent types). Else,
            check the specified parameters (server software and root listing),
            and add enum values describing them to the ip_map.
            
            Raises:
                ValueError: If the args to the class indicate nothing to scan.
            
            Returns:
                dict: A dict containing a WebServerSoftwareEnum, DirListingEnum,
                StatusEnum, and optional error status message if applicable
                for each IP passed.
        """
        if (not self.scan_root) and (not self.scan_software):
            logging.error('Invalid args: Nothing to scan.')
            raise ValueError('Invalid args: Nothing to scan.')

        for ip in self.ips:
            logging.info(f'Starting scan on {ip}. IP may change if not preserved.')
            # Check and format the IP, continue to next IP if invalid
            try:
                formatted_ip = self._format_and_validate_ip(ip)
            except ValueError:
                self.ip_map[ip] = (WEBSRVENUM.err, DIRLISTENUM.err, STATUSENUM.bad_ip, None)
                self._log_scan_complete(ip, success = False)
                continue
            # Return formatted IP or original IP if preserve_ips
            expected_ip = ip if self.preserve_ips else formatted_ip

            # Make the request, check status
            try:
                resp, status_code = self._make_request(formatted_ip)
            except requests.exceptions.RequestException as e:
                    self.ip_map[expected_ip] = (
                                    WEBSRVENUM.err,
                                    DIRLISTENUM.err,
                                    STATUSENUM.bad_request,
                                    _ERROR_STATUS_MSG.format(e)
                                    )
                    self._log_scan_complete(expected_ip, success = False)
                    continue
            if status_code != 200:
                self.ip_map[expected_ip] = (
                                WEBSRVENUM.err,
                                DIRLISTENUM.err,
                                STATUSENUM.bad_response_code,
                                _ERROR_STATUS_MSG.format(status_code)
                                )
                self._log_scan_complete(expected_ip, success = False)
                continue
    
            if self.scan_software:
                srv_type = self._server_software(resp)
            else:
                srv_type = WEBSRVENUM.disabled
            if self.scan_root:
                root_listing = self._root_listing_avail(resp)
            else:
                root_listing = DIRLISTENUM.disabled
            self.ip_map[expected_ip] = (srv_type, root_listing, STATUSENUM.good, None)
            self._log_scan_complete(expected_ip, success = True)
            
        return self.ip_map
    
    def _format_and_validate_ip(self, ip) -> str:
        """Add http to IP if needed. Raises ValueError if invalid IP."""
        # requests expects an IP with http://
        if not ip.startswith(("http://", "https://")):
            logging.debug(f'{ip} did not start with http(s)://, adding.')
            ip = "http://" + ip
        # Matches "http(s)://" prefix + IP address + optional port.
        pattern = r'^(https?://)\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?::\d{1,5})?$'
        if not re.match(pattern, ip):
            logging.error(f'{ip} is not valid.')
            raise ValueError(f'{ip} is not valid.')
        
        return ip
        
    def _make_request(self, ip: str) -> tuple[requests.Response, int]:
        """Send GET HTTP request, return it and HTTP status code. Raises RequestException."""
        try:
            logging.info(f'Sending GET request to {ip}.')
            response = requests.get(ip, timeout=_REQUEST_TIMEOUT)
        except requests.exceptions.RequestException as e:
            logging.error(f'Got request exception: {e}.')
            raise e
        logging.debug(f'Sent request to {ip}, got status {response.status_code}.')
        
        return response, response.status_code
        
    def _server_software(self, resp: requests.Response) -> WEBSRVENUM:
        """Check HTTP header server field and return the applicable enum if available."""
        # Sometimes server fields are removed from headers
        server_field = resp.headers.get('Server', None)
        if not server_field:
            logging.info('No server field in HTTP header.')
            return WEBSRVENUM.none
        logging.debug(f'HTTP "server" header field is set to: {server_field}')

        header_sw, header_ver = server_field.split('/')
        # If software and software version supported, return it. Else return "other"
        try:
            software = WEBSRVENUM[header_sw.lower()]
            logging.debug(f'{header_sw} is supported, checking version..')
        except ValueError:
            logging.warning(f'"{header_sw}" is unsupported.')
            return WEBSRVENUM.other

        # Check version. If type (above) and ver are supported, return its enum. Else other.
        # We only care about major, minor
        header_ver_major_minor = '.'.join(header_ver.split('.')[:2])
        if header_ver_major_minor in WEBSRVVERS[software]:
            logging.debug(f'{header_ver} is supported, returning {software}.')
            return software
        return WEBSRVENUM.other
    
    def _root_listing_avail(self, resp: requests.Response) -> DIRLISTENUM:
        """Very rudimentary way of seeing if files are accessible at root."""
        if 'Index of' in resp.text:
            logging.debug('Directory listing at root appears to be available.')
            return DIRLISTENUM.available
        else:
            logging.debug('Directory listing at root appears to be unavailable.')
            return DIRLISTENUM.unavailable
    
    def _log_scan_complete(self, ip: str, success: bool) -> None:
        """Log what was scanned."""
        if success == False:
            logging.warning(f'Unsuccessful scan complete: {self.ip_map[ip]}.')
        else:
            logging.info(f'Successful scan complete: {self.ip_map[ip]}.')
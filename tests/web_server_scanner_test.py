import unittest
import unittest.mock
import requests_mock
import requests
from scanner import web_server_scanner
from scanner.utils import WebSrvEnum, get_flagged_versions, DirListEnum, StatusEnum
from typing import Optional
import logging

_FAKE_IP = 'http://127.0.0.1'

logging.basicConfig(level='DEBUG')

class WebServerScannerNoInit(web_server_scanner.WebServerScanner):
    """We don't need init and its required parameters to test methods."""
    def __init__(self):
        pass
    
def create_mock_response(
    status_code: int = 200, ip: str = _FAKE_IP,
    listing: Optional[bool] = None, server_header: Optional[str] = None,
    ) -> requests.Response:
    header = {}
    if server_header:
       header['Server'] = server_header
    text = ''
    if listing:
        text = '<head><title>Index of /</title></head>'
    return requests_mock.create_response(
        request=requests.Request('GET', ip),
        text=text,
        status_code=status_code,
        headers=header,
        )

class WebServerScannerTests(unittest.TestCase):
    maxDiff = None
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        srv = 'nginx/{}'
        flagged_ver = get_flagged_versions()[WebSrvEnum.nginx][0]
        cls.flagged_srv, cls.unflagged_srv = srv.format(flagged_ver), srv.format('0')
        
    def test_scanner(self):
        """Test WebServerScanner end-to-end with list of IPs."""
        # .1 has flagged web server and root listing available, .2 has neither.
        mock_resp_1 = create_mock_response(listing=True, server_header=self.flagged_srv)
        mock_resp_2 = create_mock_response()
        # .1 formatted with port number, .2 not.
        ips = ['http://192.168.0.1:8080', '192.168.0.2']
        responses = [mock_resp_1, mock_resp_2]
        expected_1 = {
            'WebServerSoftware': WebSrvEnum.nginx,
            'RootListing': DirListEnum.available,
            'Status': StatusEnum.good,
            'ErrorMsg': None
        }
        expected_2 = {
            'WebServerSoftware': WebSrvEnum.none,
            'RootListing': DirListEnum.unavailable,
            'Status': StatusEnum.good,
            'ErrorMsg': None
        }
        expected_result = {ips[0]: expected_1, ips[1]: expected_2}

        with unittest.mock.patch.object(requests, 'get', side_effect=responses):
            # Use the real WebServerScanner in this one.
            result = web_server_scanner.WebServerScanner(ips, preserve_ips=True)()
            self.assertDictEqual(dict(result), expected_result)


    def test_scanner_err(self):
        """Test WebServerScanner end-to-end with list of IPs with errors."""
        # For .2. .1 has a bad IP so no request will be made.
        mock_resp = requests.exceptions.ConnectTimeout
        # .1 is an invalid IP, .2 times out
        ips = ['0192.168.0.1', '192.168.0.2']
        expected_1 = {
            'WebServerSoftware': WebSrvEnum.err,
            'RootListing': DirListEnum.err,
            'Status': StatusEnum.bad_ip,
            'ErrorMsg': 'Pass a valid IP.'
        }
        expected_2 = {
            'WebServerSoftware': WebSrvEnum.err,
            'RootListing': DirListEnum.err,
            'Status': StatusEnum.response_err,
            'ErrorMsg': web_server_scanner._ERROR_STATUS_MSG.format('')
        }
        expected_result = {ips[0]: expected_1, ips[1]: expected_2}

        with unittest.mock.patch.object(requests, 'get', side_effect=mock_resp):
            # Use the real WebServerScanner in this one.
            result = web_server_scanner.WebServerScanner(ips, preserve_ips=True)()
            self.assertDictEqual(dict(result), expected_result)

            
    def test_format_ip(self):
        unformatted_ip = '127.0.0.1'
        result = WebServerScannerNoInit()._format_and_validate_ip(unformatted_ip)
        self.assertEqual(result, _FAKE_IP)
        
    def test_invalid_ip(self):
        invalid_ip = '0127.0.0.1'
        invalid_host = 'example.com'
        self.assertRaises(ValueError,
                          WebServerScannerNoInit()._format_and_validate_ip, invalid_ip)
        self.assertRaises(ValueError,
                          WebServerScannerNoInit()._format_and_validate_ip, invalid_host)
        
    def test_make_request_good_resp(self):
        mock_resp = create_mock_response()
        with unittest.mock.patch.object(requests, 'get', return_value=mock_resp):
            resp = WebServerScannerNoInit()._make_request(_FAKE_IP)
        self.assertEqual(resp.text, '')
        
    def test_make_request_bad_resp(self):
        mock_resp = create_mock_response(404)
        with unittest.mock.patch.object(requests, 'get', return_value=mock_resp):
            self.assertRaises(ValueError,
                              WebServerScannerNoInit()._make_request, _FAKE_IP)
        
    def test_server_software_supported(self):
        mock_resp = create_mock_response(server_header=self.flagged_srv)
        self.assertEqual(WebServerScannerNoInit()._server_software(mock_resp),
                         WebSrvEnum.nginx)

    def test_server_software_unsupported(self):
        mock_resp = create_mock_response(server_header=self.unflagged_srv)
        self.assertEqual(WebServerScannerNoInit()._server_software(mock_resp),
                         WebSrvEnum.other)
        
    def test_root_listing_avail(self):
        mock_resp = create_mock_response(listing=True)
        self.assertEqual(WebServerScannerNoInit()._root_listing(mock_resp),
                         DirListEnum.available)

    def test_root_listing_unavail(self):
        mock_resp = create_mock_response(listing=False)
        self.assertEqual(WebServerScannerNoInit()._root_listing(mock_resp),
                         DirListEnum.unavailable)
        

if __name__ == '__main__':
    unittest.main()
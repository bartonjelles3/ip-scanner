import unittest
import web_server_scanner
import utils

class WebServerScannerNoInit(web_server_scanner.WebServerScanner):
    """We don't need init and its required parameters to test methods."""
    def __init__(self):
        pass

class WebServerScannerTests(unittest.TestCase):
    def test_format_ip(self):
        unformatted_ip = '127.0.0.1'
        expected_ip = 'http://127.0.0.1'
        scanner = WebServerScannerNoInit()
        result = scanner._format_and_validate_ip(unformatted_ip)
        self.assertEqual(result, expected_ip)
        
    def test_invalid_ip(self):
        invalid_ip = '0127.0.0.1'
        invalid_host = 'example.com'
        scanner = WebServerScannerNoInit()
        self.assertRaises(ValueError, scanner._format_and_validate_ip, invalid_ip)
        
    def test_make_request(self):
        

if __name__ == '__main__':
    unittest.main()
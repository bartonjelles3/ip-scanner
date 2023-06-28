import logging
import flask

from scanner import web_server_scanner

app = flask.Flask(__name__)

@app.route('/scan', methods=['POST'])
def scan_web_servers():
    app.logger.debug("debug log info")
    data = flask.request.get_json()
    ips = data.get('ips', [])
    scan_software = data.get('scan_software', True)
    scan_root = data.get('scan_root', True)
    preserve_ips = data.get('preserve_ips', True)
    log_level = data.get('log_level', 'WARNING')

    result = web_server_scanner.WebServerScanner(ips, scan_software, scan_root,
                                                 preserve_ips, log_level)()

    return flask.jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
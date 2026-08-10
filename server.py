#!/usr/bin/env python3
import json
import http.server
import socketserver
import os
import tempfile
import threading

PORT = 5000
BIND_ADDRESS = '0.0.0.0'
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'integravida_data.json')
DATA_LOCK = threading.Lock()
DEFAULT_DATA = {
    'attendances': [],
    'network': []
}


def read_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as data_file:
            data = json.load(data_file)
            return {
                'attendances': data.get('attendances', []) if isinstance(data, dict) else [],
                'network': data.get('network', []) if isinstance(data, dict) else []
            }
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return DEFAULT_DATA.copy()


def write_data(data):
    clean_data = {
        'attendances': data.get('attendances', []),
        'network': data.get('network', [])
    }
    directory = os.path.dirname(DATA_FILE)
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=directory,
                                     delete=False) as temporary_file:
        json.dump(clean_data, temporary_file, ensure_ascii=False, indent=2)
        temporary_file.flush()
        os.fsync(temporary_file.fileno())
        temporary_path = temporary_file.name
    os.replace(temporary_path, DATA_FILE)


class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def send_json(self, payload, status=200):
        response = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def do_GET(self):
        if self.path == '/api/data':
            with DATA_LOCK:
                self.send_json(read_data())
            return
        super().do_GET()

    def do_PUT(self):
        if self.path != '/api/data':
            self.send_error(404, 'Endpoint not found')
            return

        try:
            content_length = int(self.headers.get('Content-Length', '0'))
            request_data = json.loads(self.rfile.read(content_length).decode('utf-8'))
            if not isinstance(request_data, dict) or not isinstance(request_data.get('attendances'), list):
                raise ValueError('Invalid data format')
            with DATA_LOCK:
                write_data(request_data)
            self.send_json({'ok': True})
        except (ValueError, json.JSONDecodeError, UnicodeDecodeError, OSError):
            self.send_json({'ok': False, 'error': 'Não foi possível salvar os dados.'}, 400)


os.chdir(os.path.dirname(os.path.abspath(__file__)))

with socketserver.ThreadingTCPServer((BIND_ADDRESS, PORT), MyHTTPRequestHandler) as httpd:
    httpd.daemon_threads = True
    print(f"Server running at http://{BIND_ADDRESS}:{PORT}/")
    httpd.serve_forever()

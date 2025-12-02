#!/usr/bin/env python3
import http.server
import socketserver
import os

PORT = 5000
BIND_ADDRESS = '0.0.0.0'

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with socketserver.TCPServer((BIND_ADDRESS, PORT), MyHTTPRequestHandler) as httpd:
    print(f"Server running at http://{BIND_ADDRESS}:{PORT}/")
    httpd.serve_forever()

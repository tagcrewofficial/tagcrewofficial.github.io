#!/usr/bin/env python3
import http.server
import socketserver
import os
import sys
from functools import partial

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)
    
    def do_GET(self):
        # Handle clean URLs without .html extension
        if self.path == '/':
            self.path = '/404.html'
        if self.path == '/about':
            self.path = '/about.html'
        if self.path == '/404':
            self.path = '/404.html'
        elif self.path == '/downloads':
            self.path = '/downloads.html'
        # Call the parent method to handle the request
        super().do_GET()
    
    def end_headers(self):
        # Add CORS headers and cache control
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

if __name__ == "__main__":
    PORT = 5000
    
    # Allow socket reuse to prevent "Address already in use" errors
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("0.0.0.0", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"Server running at http://0.0.0.0:{PORT}/")
        print("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
            sys.exit(0)
#!/usr/bin/env python3
"""Local dev server with pretty-URL resolution — same clean URLs GitHub
Pages serves in production. Usage: python3 serve.py [port]  (default 8765)"""
import os, sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

ROOT = os.path.dirname(os.path.abspath(__file__))

# Pretty URL -> file. Matches _redirects.
PRETTIES = {
    "/privacy": "/privacy.html",
}

class Handler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = PRETTIES.get(path.split("?")[0], path)
        return super().translate_path(path)
    # /404 -> /404.html too
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, must-revalidate')
        if self.path.rstrip("/") == "/404" and self._headers_buffer:
            pass
        super().end_headers()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    os.chdir(ROOT)
    server = HTTPServer(("127.0.0.1", port), Handler)
    print(f"Serving {ROOT} at http://localhost:{port}/  (Ctrl+C to stop)")
    server.serve_forever()
"""
Elevation CORS proxy — bypasses opentopodata's missing CORS header
by fetching server-side instead of from browser JS.
Run with: python3 elevation_proxy.py
Runs on port 8001, alongside your existing server on port 8000.
"""

import json
import urllib.request
import urllib.parse
import urllib.error
from http.server import BaseHTTPRequestHandler, HTTPServer

UPSTREAM = "https://api.opentopodata.org/v1/srtm90m"


class ProxyHandler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path != "/elevation":
            self.send_response(404)
            self._cors()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "not found"}).encode())
            return

        query = urllib.parse.parse_qs(parsed.query)
        locations = query.get("locations", [None])[0]

        if not locations:
            self.send_response(400)
            self._cors()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "missing locations param"}).encode())
            return

        upstream_url = f"{UPSTREAM}?locations={urllib.parse.quote(locations, safe='|,.-')}"

        try:
            req = urllib.request.Request(upstream_url, headers={"User-Agent": "topo-weather-proxy/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                body = resp.read()
                status = resp.status
        except urllib.error.HTTPError as e:
            body = e.read()
            status = e.code
        except Exception as e:
            self.send_response(502)
            self._cors()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"upstream fetch failed: {e}"}).encode())
            return

        self.send_response(status)
        self._cors()
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        print(f"[proxy] {self.address_string()} - {format % args}")


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8001), ProxyHandler)
    print("Elevation proxy running at http://127.0.0.1:8001")
    server.serve_forever()
# -------------------------------
# Simple HTTP Server Demo
# -------------------------------
# This script creates a simple HTTP server that can receive and serve
# sensor data via REST API endpoints

import http.server
import socketserver
import json
from urllib.parse import urlparse, parse_qs

HOST = "localhost"
PORT = 8000

# In-memory storage for sensor data
sensor_data = {}


class Handler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler for sensor data API."""

    def do_GET(self):
        """Handle GET requests - retrieve sensor data by ID."""
        if self.path.startswith("/sensor"):
            # Parse URL query parameters
            query = urlparse(self.path).query
            params = parse_qs(query)
            sensor_id = params.get("id", [None])[0]

            if sensor_id:
                # Look up sensor data by ID
                data = sensor_data.get(sensor_id)
                if data:
                    # Return sensor data as JSON
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(json.dumps(data).encode("utf-8"))
                    return

            # Sensor not found
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
            return

    def do_POST(self):
        """Handle POST requests - store new sensor data."""
        if self.path == "/sensor":
            # Get content length and validate content type
            content_length = int(self.headers["Content-Length"])
            if self.headers.get("Content-Type") != "application/json":
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid Content-Type")
                return

            # Read and parse JSON data
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data)
                sensor_id = data.get("id")
                if not sensor_id:
                    raise ValueError("Missing 'id' in data")
                # Store sensor data in memory
                sensor_data[sensor_id] = data
            except json.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid JSON")
                return
            except ValueError as ve:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(str(ve).encode("utf-8"))
                return

            print(f"Received sensor data: {data}")
            # Send success response
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f"Data received for sensor {sensor_id}".encode("utf-8"))
        else:
            # Endpoint not found
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")


# Start the HTTP server
with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
    print(f"Serving at {HOST}:{PORT}")
    httpd.serve_forever()

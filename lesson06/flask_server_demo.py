# -------------------------------
# Simple Flask Server Demo
# -------------------------------
# This script creates a simple Flask server that can receive and serve
# sensor data via REST API endpoints

from flask import Flask, request, jsonify

# Create Flask application instance
app = Flask(__name__)

# Server configuration
HOST = "localhost"
PORT = 8000

# In-memory storage for sensor data (dictionary acts as simple database)
sensor_data = {}


@app.route("/sensor/<id>", methods=["GET"])
def get_sensor(id):
    """
    Handle GET requests - retrieve sensor data by ID.

    URL pattern: /sensor/{sensor_id}
    Example: GET /sensor/temp_001

    Returns:
        - 200: JSON data if sensor exists
        - 404: Not found if sensor doesn't exist
    """
    if id:
        # Look up sensor data in our in-memory storage
        data = sensor_data.get(id)
        if data:
            # Return JSON response with 200 status code
            return jsonify(data), 200

    # Return 404 if sensor ID not found
    return "Not Found", 404


@app.route("/sensor", methods=["POST"])
def post_sensor():
    """
    Handle POST requests - store new sensor data.

    URL pattern: /sensor
    Content-Type: application/json

    Expected JSON payload:
    {
        "id": "sensor_id",
        "temperature": 25.5,
        "unit": "celsius"
    }

    Returns:
        - 200: Success message
        - 400: Bad request (invalid JSON or missing ID)
    """
    # Check if request contains JSON data
    if not request.is_json:
        return "Invalid Content-Type", 400

    try:
        # Parse JSON data from request body
        data = request.get_json()
        sensor_id = data.get("id")

        if sensor_id:
            # Store sensor data in memory using sensor_id as key
            sensor_data[sensor_id] = data
            print(f"Received sensor data: {data}")
            return f"Data received for sensor {sensor_id}", 200
        else:
            return "Missing sensor ID", 400

    except Exception:
        # Handle JSON parsing errors
        return "Invalid JSON", 400


if __name__ == "__main__":
    # Print server info and start Flask development server
    print(f"Serving at {HOST}:{PORT}")
    print("Available endpoints:")
    print("  POST /sensor - Store sensor data")
    print("  GET /sensor/<id> - Retrieve sensor data by ID")

    # Start Flask development server with debug mode enabled
    app.run(host=HOST, port=PORT, debug=True)

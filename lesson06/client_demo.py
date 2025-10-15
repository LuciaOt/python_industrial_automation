# -------------------------------
# HTTP Client Demo
# -------------------------------
# This script demonstrates how to send HTTP requests to a server
# to POST sensor data and then retrieve it via GET requests

import requests

SERVER_URL = "http://localhost:8000"

# Send sensor data to server via POST requests
for i in range(3):
    # Create sample sensor data
    sensor_data = {
        "id": f"sensor_{i}",
        "temperature": 20 + i,
        "humidity": 50 + i * 2,
    }

    if i == 2:
        # Test invalid data (missing 'id' field)
        sensor_data.pop("id")

    # POST data to server
    response = requests.post(f"{SERVER_URL}/sensor", json=sensor_data)
    print(f"POST /sensor {response.status_code}: {response.text}")

# Retrieve sensor data from server via GET requests
for i in range(3):
    sensor_id = f"sensor_{i}"

    if i == 2:
        # Test non-existing sensor ID
        sensor_id = "sensor_999"
    # GET data from server by sensor ID
    response = requests.get(f"{SERVER_URL}/sensor/{sensor_id}")

    if response.status_code == 200:
        # Successfully retrieved data - parse JSON response
        print(f"GET /sensor?id={sensor_id} {response.status_code}: {response.json()}")
    else:
        # Error retrieving data - show error message
        print(f"GET /sensor?id={sensor_id} {response.status_code}: {response.text}")

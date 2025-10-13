# -------------------------------
# Weather API Demo using Tomorrow.io
# -------------------------------
# This script demonstrates how to fetch real-time weather data
# using the Tomorrow.io API with geographic coordinates
#
# Install requests if needed:
# pip install requests

import requests
import json
from pprint import pprint
from os import getenv

# Get API key from environment variable for security
API_KEY = getenv("API_KEY")


def get_ip():
    """Get public IP address using ipify.org API."""
    url = "https://api.ipify.org/"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Error: HTTP {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


def get_location(ip: str):
    """Get location information for an IP address in specified format."""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        if response.status_code == 200:
            json_data = response.json()
            data = json_data["lat"], json_data["lon"]
            return data
        else:
            print(f"Error: HTTP {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON parsing failed: {e}")
        return None


def get_real_time_weather(lat: float, lon: float):
    """Get real-time weather data for given latitude and longitude."""
    # Construct API URL with location and parameters
    url = (
        f"https://api.tomorrow.io/v4/weather/realtime?"
        f"location={lat},{lon}"
        f"&apikey={API_KEY}"
        "&units=metric"  # Use metric units (Celsius, km/h, etc.)
    )

    # Set request headers for optimal response
    headers = {"accept": "application/json", "accept-encoding": "deflate, gzip, br"}
    try:
        # Make GET request to the weather API
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: HTTP {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON parsing failed: {e}")
        return None


def main():
    # Coordinates for a specific location (latitude, longitude)
    print("--- Weather API Demo ---")
    ip = get_ip()
    if not ip:
        print("Failed to get public IP")
        return

    location = get_location(ip)
    if not location:
        print("Failed to get location data")
        return

    lat, lon = location

    # Fetch weather data
    weather = get_real_time_weather(lat, lon)
    if not weather:
        print("Failed to get weather data")
        return

    # Pretty print the weather data
    pprint(weather, indent=2, compact=True)


if __name__ == "__main__":
    main()

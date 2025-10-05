# -------------------------------
# IP Address Geolocation Demo
# -------------------------------
# This script demonstrates how to get your public IP address
# and retrieve location information in different formats

import requests
import json
from pprint import pprint


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


# Documentation: https://ip-api.com/docs
def get_location(ip: str, format: str):
    """Get location information for an IP address in specified format."""
    try:
        response = requests.get(f"http://ip-api.com/{format}/{ip}", timeout=5)
        if response.status_code == 200:
            data = response.text
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
    print("--- IP Address and Location Demo ---")

    # Get public IP address
    ip = get_ip()
    if not ip:
        print("Failed to get public IP")
        return

    # Get location data in JSON format
    loc = get_location(ip, "json")  # format possibilities: json, csv, xml
    print("\nJSON:")
    json_data = json.loads(loc if loc else "{}")
    pprint(json_data)

    # Get location data in CSV format
    loc = get_location(ip, "csv")
    print("\nCSV:")
    print(loc)

    # Get location data in XML format
    loc = get_location(ip, "xml")
    print("\nXML:")
    pprint(loc)


if __name__ == "__main__":
    main()

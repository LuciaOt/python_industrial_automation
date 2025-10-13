# -------------------------------
# Basic Public IP Retrieval Demo
# -------------------------------
# Simple demonstration of getting public IP address using ipify.org API

import requests
import json

host_name = "api.ipify.org"


# Documentation: https://www.ipify.org/
def get_ip():
    """Get public IP address as plain text."""
    url = f"https://{host_name}/?format=json"
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


def main():
    print("--- Public IP and Location Demo ---")

    # Get and display public IP
    ip = get_ip()
    ip_object = json.loads(ip) if ip else {}
    print(f"Response: {ip}")

    if not ip:
        print("Failed to get public IP")
        return

    print(f"Public IP: {ip}")


if __name__ == "__main__":
    main()

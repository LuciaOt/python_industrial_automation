# -------------------------------
# IP Address Geolocation Demo
# -------------------------------
# This script demonstrates how to get your public IP address
# and retrieve location information in different formats

import requests
import json
import random
from pprint import pprint
import pandas as pd
import plotly.express as px


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


def generate_ip(count):
    ip_list = []
    for _ in range(count):
        ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
        ip_list.append(ip)
    return ip_list


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


def get_location_batch(ips):
    try:
        url = "http://ip-api.com/batch"
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, headers=headers, data=json.dumps(ips), timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"Request failed: {e}")
        return None


def visualize_location(data):
    df = pd.DataFrame(data)
    fig = px.scatter_geo(
        df,
        lat="lat",
        lon="lon",
        hover_name="query",
        title="IP Address Geolocation",
        color="country",
        projection="natural earth",
    )
    fig.show()


def main():
    print("--- IP Address and Location Demo ---")

    # # Get public IP address
    # ip = get_ip()
    # if not ip:
    #     print("Failed to get public IP")
    #     return

    # # Get location data in JSON format
    # loc = get_location(ip, "json")  # format possibilities: json, csv, xml
    # print("\nJSON:")
    # json_data = json.loads(loc if loc else "{}")
    # pprint(json_data)

    # # Get location data in CSV format
    # loc = get_location(ip, "csv")
    # print("\nCSV:")
    # print(loc)

    # # Get location data in XML format
    # loc = get_location(ip, "xml")
    # print("\nXML:")
    # pprint(loc)
    ip_list = generate_ip(100)
    response = get_location_batch(ip_list)
    if not response:
        print("Failed to get location data")
        return
    location_filtered = [item for item in response if item["status"] == "success"]
    visualize_location(location_filtered)
    print("\nDone.")


if __name__ == "__main__":
    main()

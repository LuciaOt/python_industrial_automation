# -------------------------------
# REST API Demo - Public IP
# -------------------------------
# Install requests if needed:
# pip install requests
# docs: https://requests.readthedocs.io/en/latest/

import requests


def main():
    print("--- Public IP Address Demo ---")

    try:
        # Make GET request to the API endpoint
        response = requests.get("https://api.ipify.org/", timeout=5)

        # Check if request was successful (status code 200)
        if response.status_code == 200:
            # Return the IP address as text
            my_api = response.text.strip()
            print(f"Your public IP: {my_api}")
        else:
            print(f"Error: HTTP {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")


if __name__ == "__main__":
    main()

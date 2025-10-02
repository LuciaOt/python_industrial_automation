# -------------------------------
# REST API Demo - Public IP
# -------------------------------
# Install requests if needed:
# pip install requests

import requests


def main():
    print("--- Public IP Address Demo ---")

    try:
        # Make GET request to the API endpoint
        response = requests.get("https://api.ipify.org/", timeout=5)

        # Check if request was successful (status code 200)
        if response.status_code == 200:
            # Return the IP address as text
            return response.text.strip()
        else:
            print(f"Error: HTTP {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


if __name__ == "__main__":
    main()

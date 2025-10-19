import requests
import pandas as pd
import matplotlib.pyplot as plt

# API endpoint URL
url = "https://data.csu.gov.cz/api/dotaz/v1/data/vybery/CRUHVD1T2"

# Send the request to the API
try:
    response = requests.get(url)

    # Check if the response is successful (status code 200)
    response.raise_for_status()

    # Parse the JSON response
    data = response.json()

    # Check the structure of the response to extract data
    print("Response Keys:", data.keys())

    # Extract data from the 'value' key (assuming the list is under 'value')
    if 'value' in data:
        dataset = data['value']

        # Print a sample of the data to inspect its structure
        print("Sample of Data:", dataset[:5])

        # Create a DataFrame with dummy categories as index
        df = pd.DataFrame(dataset, columns=['Value'])
        df['Category'] = [f'Category {i+1}' for i in range(len(df))]

        # Print the first few rows to verify the structure
        print(df.head())

        # Visualization: Plot a bar chart of the data
        plt.figure(figsize=(10, 6))
        plt.bar(df['Category'], df['Value'], color='skyblue', edgecolor='blue')
        plt.title('Data Visualization', fontsize=16)
        plt.xlabel('Category', fontsize=12)
        plt.ylabel('Value', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    else:
        print("No 'value' key found in the response.")

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")

except ValueError as e:
    print("Failed to decode JSON.")
    print(response.text[:500])  # Print the response text for debugging

except Exception as e:
    print(f"Unexpected error: {e}")

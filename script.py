import requests
import json
import csv
import os

def read_token_from_file(file_name="token.txt"):
    """
    Reads the Bearer token from a specified text file.
    
    Returns:
        str: The token content, stripped of whitespace.
        
    Raises:
        FileNotFoundError: If the token file is not found.
    """
    try:
        # 'r' mode for reading
        with open(file_name, 'r') as f:
            # Read the first line and strip any leading/trailing whitespace (like newlines)
            token = f.read().strip()
        return token
    except FileNotFoundError:
        # Custom error message for the user
        print(f"ERROR: Token file '{file_name}' not found in the current directory.")
        raise
    except Exception as e:
        print(f"An unexpected error occurred while reading the token file: {e}")
        raise

def fetch_and_save_transactions():
    """
    Fetches transaction data from the Watchtower API and saves relevant fields to a CSV file.
    """
    
    # 1. Read the Bearer token from the file
    try:
        bearer_token = read_token_from_file()
    except FileNotFoundError:
        # Stop execution if the file is missing
        return

    url = "https://watchtower-service.kudi.ai/data-hub/transactions/beta"

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        # 2. Use the token read from the file
        "authorization": f"{bearer_token}", 
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://watchtower.kudi.ai",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://watchtower.kudi.ai/",
        "sec-ch-ua": '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    }

    payload = {
        "filters": [
            {
                "field": "timeCreated",
                "operation": "between",
                "type": "timestamp",
                "value": {
                    "start": "2025-10-04T00:00:00Z",
                    "end": "2025-10-04T23:59:59Z"
                },
            },
            {
                "field": "meta.paymentVendor",
                "operation": "equal",
                "type": "string",
                "value": "OPAY",
            },
        ],
        "limit": 50,
        "type": "online_checkout",
    }

    print("Sending request to the API...")
    try:
        # The requests library handles converting the payload dictionary to a JSON string
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()

        response_data = response.json()
        
        # Safely access the nested list, defaulting to an empty list
        transaction_list = response_data.get("data", {}).get("list", [])

        if not transaction_list:
            print("Response received, but the transaction list is empty. No CSV file will be created.")
            return

        # Define CSV file details
        output_dir = "output"
        csv_file_name = "transactions.csv"
        csv_headers = ["_id", "paymentVendorReference"]
        
        # 1. Create the full file path: "output/transactions.csv"
        full_path = os.path.join(output_dir, csv_file_name)
        
        # 2. Create the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            # os.makedirs creates the directory and any necessary parent directories
            os.makedirs(output_dir)
            print(f"Created directory: {output_dir}")
        print(f"Found {len(transaction_list)} transactions. Writing to {csv_file_name}...")
        
        with open(full_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Write the header row
            writer.writerow(csv_headers)
            
            # Write the data rows
            for item in transaction_list:
                # Use .get() to safely access keys, providing None if a key is missing
                row = [
                    item.get("_id"),
                    item.get("paymentVendorReference")
                ]
                writer.writerow(row)
        
        print(f"Successfully created {csv_file_name}.")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - {response.text}")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred during the request: {err}")
    except (KeyError, TypeError) as json_err:
        print(f"Error parsing the JSON response or unexpected structure: {json_err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Run the function
if __name__ == "__main__":
    fetch_and_save_transactions()
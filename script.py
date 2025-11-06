import requests
import json
import datetime
import csv
import os

from util import generate_timestamped_filename, read_ids_from_file, read_token_from_file
from util import STATUS_CODES

baseUrl = "https://watchtower-service.kudi.ai/"
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    # 2. Use the token read from the file
    "authorization": "",# f"{bearer_token}", 
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

    url = baseUrl + "data-hub/transactions/beta"
    headers["authorization"] = bearer_token;



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

def fetch_and_save_payouts_transactions():
    """
    Fetches transaction data from the Watchtower API and saves relevant fields to a CSV file.
    Transactions are fetched from the payment-service.payment-service-transactions collection which is where payment-service
    and payouts-service save transactiosn before calling the vendor.

    

    :raises FileNotFoundError: If the token file is not found.
    :raises requests.exceptions.HTTPError: If a bad status code is received.
    :raises requests.exceptions.RequestException: If an error occurs during the request.
    :raises (KeyError, TypeError): If an unexpected JSON structure is encountered.
    :raises Exception: If an unexpected error occurs.
    """
    references = read_ids_from_file("references.txt")
    print(f"Successfully read {len(references)} References:")

    # 1. Read the Bearer token from the file
    try:
        bearer_token = read_token_from_file()
    except FileNotFoundError:
        # Stop execution if the file is missing
        return

    url = baseUrl + "payment-service/transactions?parentReference=POS-TRANSFER-E464E-19211f19-88b8-411f-b380-ba6af1a0c93e"
    headers["authorization"] = bearer_token;
    transaction_list = []

    # Iterate over each Reference ID in the list
    for reference in references:
        print(f"Sending request to the API... for {reference}")
        try:
            # The requests library handles converting the payload dictionary to a JSON string
            response = requests.get(url, headers=headers, timeout=30)
            # Raise an exception for bad status codes (4xx or 5xx)
            response.raise_for_status()

            response_data = response.json()
            
            # Safely access the nested list, defaulting to an empty list
            # transaction_list = response_data.get("data", {}).get("list", [])
            records = response_data.get("data", [])

            if records:
                # print("Response received, but the transaction list is empty. No CSV file will be created.")
                transaction_list.extend(records)

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err} - {response.text}")
        except requests.exceptions.RequestException as err:
            print(f"An error occurred during the request: {err}")

    try:
        # Define CSV file details
        output_dir = "output"
        csv_file_name = generate_timestamped_filename("payment_transactions")
        csv_headers = ["createdAt","_id","parentReference", "status", "statusCode","vendorReference","vendor"]
        
        # 1. Create the full file path: "output/transactions.csv"
        full_path = os.path.join(output_dir, csv_file_name)
        
    #     # 2. Create the output directory if it doesn't exist
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
                response = item.get("response",{})
                status = item.get("status","Nil")
                statusCode = ""
                vendorReference = ""
                vendor = item.get("vendor")
                if response is not None:
                    if vendor == "etranzact":
                        statusCode = response.get("responseCode","")
                        vendorReference = item.get("sessionId")
                    else:
                        statusCode = response.get("statusCode","")
                        vendorReference = item.get("vendorReference","")

                    
                row = [
                    item.get("createdAt"),
                    item.get("_id"),
                    item.get("parentReference"),
                    status,
                    statusCode,
                    # STATUS_CODES.get(statusCode,""),
                    vendorReference,
                    vendor
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
    # fetch_and_save_transactions()
    fetch_and_save_payouts_transactions()
    # read_ids_from_file("references.txt")
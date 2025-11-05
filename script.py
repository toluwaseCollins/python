import requests
import json
import csv

def fetch_and_save_transactions():
    """
    Fetches transaction data from the Watchtower API and saves relevant fields to a CSV file.
    """
    url = "https://watchtower-service.kudi.ai/data-hub/transactions/beta"

    # The long authorization token is stored in a separate variable for clarity
    bearer_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJKNGRPRDF2Nlo5R1VYejRGdjRxRW1tYlVhWnRwMnNfUGVKY3lSQ2tEaXpFIn0.eyJleHAiOjE3NjIzNTY3MjUsImlhdCI6MTc2MjM1MzEyNSwiYXV0aF90aW1lIjoxNzYyMzM4ODM3LCJqdGkiOiJlOTA3Y2FmNy04YzFhLTQ3NGYtYWNjNi02ZjljYTJjNDA1OTkiLCJpc3MiOiJodHRwczovL2tleWNsb2FrLmt1ZGkuYWkvYXV0aC9yZWFsbXMvTm9tYmEiLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiMGJjZDBmMzAtNWYwZi00MGU3LWE0ZDItZjg2ODkxZWUzMmRkIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoid2F0Y2h0b3dlci5rdWRpLmFpIiwibm9uY2UiOiI4OTFiNzQwNS1mYzU2LTQxN2YtOTA0OC1kNDZkMDYxZGQ5OGUiLCJzZXNzaW9uX3N0YXRlIjoiN2E1YzZkM2YtYmJkYy00ZTkxLWIzZTUtMTk4MThiMzRkNzA1IiwiYWNyIjoiMCIsImFsbG93ZWQtb3JpZ2lucyI6WyJodHRwczovL3dhdGNodG93ZXItc2VydmljZS1kcmMubm9tYmEuY2QiLCJodHRwczovL3dhdGNodG93ZXItc2VydmljZS5ub21iYS5jZCIsImh0dHBzOi8vd2F0Y2h0b3dlci5ub21iYS5jZCIsImh0dHBzOi8vd2F0Y2h0b3dlci51c2Vub21iYS5jb20iLCJodHRwczovL3dhdGNodG93ZXItc2VydmljZS5rdWRpLmFpIiwiaHR0cHM6Ly93YXRjaHRvd2VyLmt1ZGkuYWkiLCJodHRwczovL3dhdGNodG93ZXItc2VydmljZS51c2Vub21iYS5jb20iLCJodHRwczovL3dhdGNodG93ZXItZHJjLm5vbWJhLmNkIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwibmFtZSI6IlRvbHV3YWxhc2UgQ29sbGlucyIsInByZWZlcnJlZF91c2VybmFtZSI6InRvbHV3YXNlLmNvbGxpbnNAbm9tYmEuY29tIiwiZ2l2ZW5fbmFtZSI6IlRvbHV3YWxhc2UiLCJmYW1pbHlfbmFtZSI6IkNvbGxpbnMiLCJlbWFpbCI6InRvbHV3YXNlLmNvbGxpbnNAbm9tYmEuY29tIn0.fDPdZgRpWiJpf7g8cI5zUGA1SJYKruMwNy7c-lOHuhzyo7MdFoQUy_Zmj2Rqjspxq7_NtiQw0UIX4XwWWpZ4kkHHNaCGAcJu5HJwKW0mIxDlcCw8JiL-PgFD67RezQNnHO8pu-p9DPSwWQlkmW4XK1fj6LIGqLMPYE0zybRMzXBbKJSjOfXIMCoeSQEeEK6bW7k6kqK46MKUQEn_mM_VnWT8C3r1mH6g1gGCo-m3hbaFO-XR9kXcJ0b8JueoRCYUlPoxvIJ0SgarSCZi2jzYKVW7JMqqt2g3ZVE3S133lw8qioAJ7KPH6FoKiYadnrT6ExzRZ1DMO3mcFnZkO-X8Kw"

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": f"Bearer {bearer_token}",
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
        csv_file_name = "transactions.csv"
        csv_headers = ["_id", "paymentVendorReference"]
        
        print(f"Found {len(transaction_list)} transactions. Writing to {csv_file_name}...")
        
        with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
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
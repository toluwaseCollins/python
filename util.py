import os

STATUS_CODES = {
        "00": "Approved or completed successfully",
        "01": "Status unknown, please wait for settlement report",
        "03": "Invalid Sender",
        "05": "Do not honor",
        "06": "Dormant Account",
        "07": "Invalid Account",
        "08": "Account Name Mismatch",
        "09": "Request processing in progress",
        "12": "Invalid transaction",
        "13": "Invalid Amount",
        "14": "Invalid Batch Number",
        "15": "Invalid Session or Record ID",
        "16": "Unknown Bank Code",
        "17": "Invalid Channel",
        "18": "Wrong Method Call",
        "21": "No action taken",
        "25": "Unable to locate record",
        "26": "Duplicate record",
        "30": "Format error",
        "34": "Suspected fraud",
        "35": "Contact sending bank",
        "51": "No sufficient funds",
        "57": "Transaction not permitted to sender",
        "58": "Transaction not permitted on channel",
        "61": "Transfer limit Exceeded",
        "63": "Security violation",
        "65": "Exceeds withdrawal frequency",
        "68": "Response received too late",
        "69": "Unsuccessful Account/Amount block",
        "70": "Unsuccessful Account/Amount unblock",
        "71": "Empty Mandate Reference Number",
        "91": "Beneficiary Bank not available",
        "92": "Routing error",
        "94": "Duplicate transaction",
        "96": "System malfunction",
        "97": "Timeout waiting for response from destination",
        "": "Unknown"  # Handles the case where the code might be empty/not available
    }

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

def read_ids_from_file(file_path: str) -> list[str]:
    """
    Reads a file where each line contains a single ID and returns a list
    of those IDs, stripped of any leading or trailing whitespace.

    Args:
        file_path: The path to the file containing the IDs.

    Returns:
        A list of strings, where each string is an ID from the file.
    """
    ids = []
    try:
        # Use 'with open' for safe file handling
        with open(file_path, 'r', encoding='utf-8') as file:
            # Iterate over each line in the file
            for line in file:
                # Use .strip() to remove leading/trailing whitespace, including the newline character
                clean_id = line.strip()
                
                # Only add non-empty lines (useful for ignoring blank lines in the file)
                if clean_id:
                    ids.append(clean_id)
        return ids
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
        return []

def generate_timestamped_filename(prefix = "transactions"):
    """
    Generates a filename string with the format "transaction_yyyy_MM_dd_HH_mm_ss".
    """
    
    # 1. Get the current date and time
    now = datetime.datetime.now()
    
    # 2. Format the datetime object into the desired string format: "yyyy_MM_dd_HH_mm_ss"
    # %Y: 4-digit year (e.g., 2025)
    # %m: 2-digit month (e.g., 10)
    # %d: 2-digit day (e.g., 05)
    # %H: 2-digit hour (24-hour clock)
    # %M: 2-digit minute
    # %S: 2-digit second
    timestamp = now.strftime("%Y_%m_%d_%H_%M_%S")
    
    # 3. Combine the prefix and the timestamp
    file_name = f"{prefix}_{timestamp}.csv"
    
    return file_name

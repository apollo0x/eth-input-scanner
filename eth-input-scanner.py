import json
import requests
import re

# Function to convert hex to utf-8
def hex_to_utf8(hex_str):
    try:
        if hex_str.startswith('0x'):
            hex_str = hex_str[2:]  # Remove the '0x' prefix
        return bytes.fromhex(hex_str).decode('utf-8')
    except Exception as e:
        return f"Unable to decode: {e}"

# Function to check for human-readable text
def contains_human_readable(text):
    pattern = r'[a-zA-Z]{5,}'
    return re.search(pattern, text) is not None

# URL from Etherscan API for fetching transaction data for a specific Ethereum address
api_key = input("Enter API Key: ")
# uncomment above if you want to ask
eth_address = input("Enter Ethereum Address: ")

# URL from Etherscan API for fetching transaction data for a specific Ethereum address
url = "https://api.etherscan.io/api?module=account&action=txlist&address=" + eth_address + "&startblock=0&endblock=99999999&sort=asc&apikey=" + api_key

# Make a GET request to fetch json
response = requests.get(url)
data = response.json()  # Parse the JSON string into a Python dictionary

filtered_transactions = []
total_transactions = 0
displayed_transactions = 0

# Check for a successful response
if data["status"] == "1":
    transactions = data["result"]
    total_transactions = len(transactions)

    # Process and filter transactions
    for tx in transactions:
        utf8_input = hex_to_utf8(tx['input'])

        # Skip transactions that couldn't be decoded
        if utf8_input.startswith("Unable to decode"):
            continue

        if contains_human_readable(utf8_input):
            displayed_transactions += 1
            print(f"Block Number: {tx['blockNumber']}")
            print(f"Time Stamp: {tx['timeStamp']}")
            print(f"Hash: {tx['hash']}")
            print(f"From: {tx['from']}")
            print(f"To: {tx['to']}")
            print(f"Value: {tx['value']}")
            print(f"Gas: {tx['gas']}")
            print(f"Gas Price: {tx['gasPrice']}")
            print(f"Is Error: {tx['isError']}")
            print(f"Confirmation: {tx['confirmations']}")
            print(f"Input Data (UTF-8): {utf8_input}")
            print("-----")

            # Add to filtered transactions
            filtered_transactions.append(tx)

    # Save the filtered transaction data to a JSON file
    with open("filtered_etherscan_transactions_with_input.json", "w") as f:
        json.dump(filtered_transactions, f, indent=4)

    print(f"Saved {len(filtered_transactions)} transactions to filtered_etherscan_transactions_with_input.json")

else:
    print("Failed to retrieve transactions.")

print(f"Total transactions found: {total_transactions}")
print(f"Total transactions displayed: {displayed_transactions}")


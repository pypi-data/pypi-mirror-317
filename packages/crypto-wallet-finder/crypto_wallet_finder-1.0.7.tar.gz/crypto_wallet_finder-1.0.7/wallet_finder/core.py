"""
Core functionality for wallet finding operations.
"""

import os
import csv
import time
import uuid
import json
import platform
import itertools
import multiprocessing
from pathlib import Path

import requests
from crypto_wallet import CryptoWallet

config = {}
start_time = time.time()
app_dir_path = Path.home() / ".wallet_finder"
config_file = app_dir_path / "config.json"

with open('wordlist.txt', 'r', encoding='utf-8') as file:
    wordlist = file.read().splitlines()
    file.close()

with open('target_addresses.txt', 'r', encoding='utf-8') as file:
    target_addresses = file.read().splitlines()
    file.close()

with open('output.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Seed Phrase", "TRX Address"])
    file.close()

csv_file = open('output.csv', 'a', encoding='utf-8')
csv_file_writer = csv.writer(csv_file)

combinations = itertools.permutations(wordlist, 12)
def check_combination(seeds):
    """
    Check if the combination of seeds generates a valid TRX address
    """
    seed_phrase = ' '.join(seeds)
    try:
        wallet = CryptoWallet(seed_phrase)
        for index in range(5):
            address = wallet.get_trx_address(index)
            if address in target_addresses:
                return (seed_phrase, address)
    except ValueError:
        pass
    return None

def start_process():
    """
    Start the process of checking all combinations
    """
    valid_addresses = 0
    with multiprocessing.Pool() as pool:
        for idx, result in enumerate(pool.imap_unordered(check_combination, combinations)):
            print(f"Checked {idx} combinations")
            if not result:
                continue
            
            seed_phrase, address = result
            print(f"Found address: {address} with seed: {seed_phrase}")
            csv_file_writer.writerow([seed_phrase, address])
            valid_addresses += 1
            if valid_addresses >= len(target_addresses):
                pool.terminate()
                break
    
    csv_file.close()
    print('Total time taken:', time.time() - start_time)

def validate_device() -> bool:
    """
    Validate the device with the API key.

    This function sends a POST request to the API to validate the device with the provided API key.


    Returns:
        bool: True if the device is validated; False otherwise.

    Raises:
        Exception: If the request fails or an error occurs during the validation process
    """
    request_data = {
        "device_id": config.get("device_id"),
        "device_mac": config.get("device_mac"),
        "device_name": config.get("device_name")
    }

    if config.get("api_key"):
        request_data["api_key"] = config.get("api_key")

    try:
        response = requests.post("https://us-central1-crypto-wallet-recovery.cloudfunctions.net/gcp-wallet-finder-validate-device", json=request_data, timeout=120)
    except requests.exceptions.RequestException as e:
        print("Device validation failed: %s", e)
        raise ConnectionError("Device validation failed. Please check your internet connection.")
    
    response_data = response.json()
    print(f"Device validation response: {json.dumps(response_data, indent=4)}")

    if response.status_code == 201:
        config["api_key"] = response_data.get("api_key")
        save_config()

    return response_data.get("success", False), response_data.get("message", "Unknown Error"), response.status_code

def get_config() -> None:
    """
    Retrieve configuration data from the config.json file.

    If the configuration file does not exist, it creates a new one with default settings.

    Returns:
        dict: The loaded or default configuration data.
    """
    global config
    if os.path.exists(config_file):
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
    else:
        # Save default configuration to the file
        config = {
            "device_id": str(uuid.uuid4()),
            "device_mac": hex(uuid.getnode()),
            "device_name": platform.node(),
            "progress": 0,
            "wordlist_file": ""
        }
        save_config()

def save_config() -> None:
    """
    Save the current configuration data to the config.json file.

    This function updates the configuration file with the current settings.
    """
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

def main():
    """
    Main function to start the wallet finder process.
    """
    multiprocessing.freeze_support()
    get_config()
    status, msg, _status_code = validate_device()
    if not status:
        print(f"Device validation failed: {msg}")
        exit(1)

    start_process()

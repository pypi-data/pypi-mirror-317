"""
Core functionality for wallet finding operations.
"""

import os
import csv
import uuid
import json
import platform
import itertools
import multiprocessing
from pathlib import Path

import requests
from .crypto_wallet import CryptoWallet



class Core:
    def __init__(self):
        self.valid_addresses = 0
        self.config = {}
        self.app_dir_path = Path.home() / ".wallet_finder"
        self.app_dir_path.mkdir(parents=True, exist_ok=True)
        self.app_download_path = Path.home() / "Downloads"
        self.config_file = self.app_dir_path / "config.json"

        with open('wordlist.txt', 'r', encoding='utf-8') as file:
            self.wordlist = file.read().splitlines()

        with open('target_addresses.txt', 'r', encoding='utf-8') as file:
            self.target_addresses = file.read().splitlines()

        with open(self.app_download_path / 'output.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Seed Phrase", "TRX Address"])

        self.csv_file = open(self.app_download_path / 'output.csv', 'a', encoding='utf-8')
        self.csv_file_writer = csv.writer(self.csv_file)

    def check_combination(self, seeds):
        """
        Check if the combination of seeds generates a valid TRX address
        """
        seed_phrase = ' '.join(seeds)
        try:
            wallet = CryptoWallet(seed_phrase)
            for index in range(5):
                address = wallet.get_trx_address(index)
                if address in self.target_addresses:
                    return (seed_phrase, address)
        except ValueError:
            pass
        return None

    def start_process(self) -> None:
        """
        Start the process of checking all combinations
        """
        combinations = itertools.permutations(self.wordlist, 12)
        with multiprocessing.Pool() as pool:
            for idx, result in enumerate(pool.imap_unordered(self.check_combination, itertools.islice(combinations, self.config["progress"], None)), self.config["progress"]):
                print(f"Checked {idx} combinations")
                if not result:
                    continue
                
                seed_phrase, address = result
                print(f"Found address: {address} with seed: {seed_phrase}")
                self.csv_file_writer.writerow([seed_phrase, address])
                self.valid_addresses += 1
                if self.valid_addresses >= len(self.target_addresses):
                    pool.terminate()
                    self.csv_file.close()
                    break

                self.config["progress"] = idx
                self.save_config()

    def validate_device(self) -> bool:
        """
        Validate the device with the API key.

        This function sends a POST request to the API to validate the device with the provided API key.


        Returns:
            bool: True if the device is validated; False otherwise.

        Raises:
            Exception: If the request fails or an error occurs during the validation process
        """
        request_data = {
            "device_id": self.config.get("device_id"),
            "device_mac": self.config.get("device_mac"),
            "device_name": self.config.get("device_name")
        }

        if self.config.get("api_key"):
            request_data["api_key"] = self.config.get("api_key")

        try:
            response = requests.post("https://us-central1-crypto-wallet-recovery.cloudfunctions.net/gcp-wallet-finder-validate-device", json=request_data, timeout=120)
        except requests.exceptions.RequestException as e:
            print("Device validation failed: %s", e)
            raise ConnectionError("Device validation failed. Please check your internet connection.")
        
        response_data = response.json()
        print(f"Device validation response: {json.dumps(response_data, indent=4)}")

        if response.status_code == 201:
            self.config["api_key"] = response_data.get("api_key")
            self.save_config()

        return response_data.get("success", False), response_data.get("message", "Unknown Error"), response.status_code

    def get_config(self) -> None:
        """
        Retrieve configuration data from the config.json file.

        If the configuration file does not exist, it creates a new one with default settings.

        Returns:
            dict: The loaded or default configuration data.
        """
        if os.path.exists(self.config_file):
            with open(self.config_file, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        else:
            # Save default configuration to the file
            self.config = {
                "device_id": str(uuid.uuid4()),
                "device_mac": hex(uuid.getnode()),
                "device_name": platform.node(),
                "progress": 0,
                "wordlist_file": ""
            }
            self.save_config()

    def save_config(self) -> None:
        """
        Save the current configuration data to the config.json file.

        This function updates the configuration file with the current settings.
        """
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4)

    def main(self) -> None:
        """
        Main function to start the wallet finder process.
        """
        multiprocessing.freeze_support()
        self.get_config()
        status, msg, _status_code = self.validate_device()
        if not status:
            print(f"Device validation failed: {msg}")
            exit(1)

        self.start_process()

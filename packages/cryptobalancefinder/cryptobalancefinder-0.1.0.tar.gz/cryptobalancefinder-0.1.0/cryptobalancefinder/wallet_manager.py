"""
This module provides the WalletManager class for managing cryptocurrency wallets and their balances.
"""

import os
import sys
import json
import time
import asyncio
import logging
import platform
import argparse
import itertools
from pathlib import Path
from argparse import Namespace
from typing import Optional, Dict, List
from logging.handlers import RotatingFileHandler

import yaml
from .crypto_wallet import CryptoWallet
from .balance_checker import AsyncBalanceChecker


class WalletManager:
    """Manage cryptocurrency wallets and their balances."""

    def __init__(self, config_path: Optional[str] = None, batch_size: int = 25, 
                 logger: Optional[logging.Logger] = None) -> None:
        """
        Initialize the WalletManager.

        Args:
            config_path (str, optional): Path to config file. Defaults to None.
            batch_size (int, optional): Batch size for balance checks. Defaults to 25.
            logger (logging.Logger, optional): Logger for output. Defaults to None.
        """
        self.logger = logger or logging.getLogger(__name__)
        self.data: List[Dict] = []
        self.total_valid_seeds = 0
        self.account_with_balance = 0
        self.balance = False
        self.batch_size = batch_size
        
        # Load configuration
        self.config = self._load_config(config_path) if config_path else {}
        self.balance_checker = AsyncBalanceChecker(
            tron_api_url=self.config.get('api_keys', {}).get('tron_grid', []),
            logger=self.logger
        )

    def _load_config(self, config_path: str) -> dict:
        """
        Load configuration from a YAML file.

        Args:
            config_path (str): Path to the configuration file.

        Returns:
            dict: Configuration data.
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.error("Failed to load config: %s", str(e))
            return {}

    def get_wallet(self, seed_phrase: str) -> dict:
        """
        Create a wallet from a seed phrase and get its addresses.

        Args:
            seed_phrase (str): The seed phrase to generate addresses from.

        Returns:
            dict: Dictionary containing wallet addresses.

        Raises:
            ValueError: If no addresses are found for the seed phrase.
        """
        wallet = CryptoWallet(seed_phrase)
        addresses = wallet.get_trx_address()

        if not addresses:
            raise ValueError("No addresses found")

        self.total_valid_seeds += 1
        self.logger.info("Valid seed phrase: %s", seed_phrase)
        return addresses

    async def check_balance(self, wallets: List[dict]) -> None:
        """
        Check balances for a list of wallets.

        Args:
            wallets (List[dict]): List of wallet information to check.
        """
        try:
            wallets_result = await self.balance_checker.check_alls(wallets, self.batch_size)

            for wallet in wallets_result:
                if any(wallet['balances'].values()):
                    self.account_with_balance += 1
                    self.balance = True
                    self.data.append(wallet)
                    self.logger.info("Wallet with balance: %s", wallet)

            if self.balance:
                self.save_data()

        except Exception as e:
            self.logger.error("Failed to check balances: %s", str(e))

        finally:
            self.balance = False

    def save_data(self, output_file: str = "accounts_with_balance.json") -> None:
        """
        Save wallet data to a JSON file.

        Args:
            output_file (str, optional): Output file path. Defaults to "accounts_with_balance.json".
        """
        try:
            with open(output_file, "w", encoding='utf-8') as f:
                json.dump(self.data, f, indent=4)
            self.logger.info("Data saved to %s", output_file)
        except Exception as e:
            self.logger.error("Failed to save data: %s", str(e))


def start(arguments: Namespace, logger: logging.Logger) -> None:
    """Main function to process the seeds."""
    wallet_manager = WalletManager(arguments.batch_size, logger)

    if arguments.wordlist and not arguments.filename:
        raise ValueError("Please provide a wordlist file")

    wordlist = load_wordlist() if not arguments.wordlist else load_wordlist(arguments.filename)
    combinations = itertools.permutations(wordlist, 12)

    start_index = 0 if not arguments.start else arguments.start
    wallets = []

    for index, seeds in enumerate(itertools.islice(combinations, start_index, None), start=start_index):
        # Normalize seeds
        seeds = list(map(lambda x: x.lower().strip(), seeds))
        seeds = " ".join(seeds)

        try:
            wallet = wallet_manager.get_wallet(seeds)
            wallets.append(wallet)  # Accumulate wallet addresses

        except ValueError as e:
            logger.debug("Error occurred: %s", str(e))

        # Display progress every 20 seeds checked
        if index % 20 == 0:
            # Clear the console
            os.system('cls' if os.name == 'nt' else 'clear')
            # Display the progress, total valid seeds, and total accounts with balance
            formatted_total_valid_seeds = "{:,}".format(
                wallet_manager.total_valid_seeds)
            formatted_account_with_balance = "{:,}".format(
                wallet_manager.account_with_balance)
            formatted_index = "{:,}".format(index)
            formatted_start_index = "{:,}".format(start_index)
            print(f"Processing Seed: {seeds}")
            print(
                f"Total Accounts with Balance: {formatted_account_with_balance}")
            print(f"Total Valid Seeds: {formatted_total_valid_seeds}")
            print(f"Checking Wallet: {formatted_index}")
            print(f"Start from Index: {formatted_start_index}", end="\n\n")

        if len(wallets) >= arguments.batch_size:  # Check balances in batches of 25
            try:
                # Pass only the first 25 wallets
                asyncio.run(wallet_manager.check_balance(wallets))

            except Exception as e:
                logger.error("Failed to check balances for batch: %s",
                                str(e))
            # Remove the processed wallets from the list
            wallets = wallets[arguments.batch_size:]

            # Sleep for a while to avoid rate limiting
            time.sleep(0.3)

    # Process any remaining wallets
    if wallets:
        wallet_manager.check_balance(wallets)


def load_wordlist(filename='bip39_wordlist.txt') -> list:
    """
    Load a custom wordlist from a file.

    Args:
        filename (str): The file name containing the wordlist.

    Returns:
        list: The loaded wordlist.
    """
    with open(filename, 'r', encoding="utf-8") as f:
        return f.read().splitlines()


def argument_parser_config() -> Namespace:
    """Parse the command-line arguments."""
    argument_parser = argparse.ArgumentParser(
        description="Crypto cold wallet finder and check for the balance", add_help=True)
    argument_parser.add_argument(
        '-w', "--wordlist", help="Use custom wordlist", action="store_true", default=False)
    argument_parser.add_argument(
        '-f', "--filename", help="Custom wordlist filename include full path", type=str)
    argument_parser.add_argument(
        '-s', "--start", help="Start index of the seed", type=int)
    argument_parser.add_argument(
        '-d', "--debug", help="Enable debug mode", action="store_true", default=False)
    argument_parser.add_argument(
        '-b', '--batch-size', help="Batch size for checking balances", type=int, default=25)

    return argument_parser.parse_args()


def setup_logger(arguments: Namespace, log_file_path: Path) -> logging.Logger:
    """
    Setup the logger.
    """
    # Set up the logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO if not arguments.debug else logging.DEBUG)

    max_log_size = 25 * 1024 * 1024  # 25 MB
    backup_count = 5  # Keep last 5 log files

    # Log message format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # File Handler for persistent logging
    file_handler = RotatingFileHandler(log_file_path, maxBytes=max_log_size, backupCount=backup_count)
    file_handler.setLevel(logger.level)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


def main(arguments: Namespace) -> None:
    """Main function to initialize the script."""
    system = platform.system().lower()

    # Determine platform-specific log directory
    if system == 'windows':
        app_data_dir = Path(os.getenv('APPDATA', Path.home() /
                                      'AppData' / 'Roaming')) / 'CryptoWalletRecoveryApp'
    elif system == 'darwin':  # macOS
        app_data_dir = Path.home() / 'Library' / 'Logs' / 'CryptoWalletRecoveryApp'
    else:  # Linux and other UNIX-based systems
        app_data_dir = Path.home() / '.crypto_wallet_recovery'

    # Download directory
    download_dir = Path.home() / 'Downloads'
    log_file_path = app_data_dir / 'logs'

    # Ensure log directory exists
    app_data_dir.mkdir(parents=True, exist_ok=True)
    download_dir.mkdir(parents=True, exist_ok=True)
    log_file_path.mkdir(parents=True, exist_ok=True)

    log_file_path = log_file_path / 'wallet_recovery.log' if not arguments.debug else Path.cwd() / 'wallet_recovery.log'

    # Check if the log file exists and the script is not running in a frozen state (e.g., packaged with PyInstaller)
    if log_file_path.exists() and not getattr(sys, 'frozen', False):
        log_file_path.unlink()

    logger = setup_logger(arguments, log_file_path)

    # Log the initialization and OS details
    logger.info("Logging initialized. Log file is located at: %s", log_file_path)
    logger.info("Running on %s %s", platform.system(), platform.release())

    logger.info("Arguments: %s", arguments)
    logger.info("App data directory: %s", app_data_dir)
    logger.info("Download directory: %s", download_dir)

    try:
        start(arguments, logger)
    except Exception as e:
        logger.exception("Error occurred: %s", str(e),
                         exc_info=e, stack_info=True)
        sys.exit(1)
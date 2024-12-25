"""
This module contains a class to check the balance of multiple addresses asynchronously.
The class uses the `aiohttp` library to make asynchronous HTTP requests to the Tron APIs.
"""

import logging
import asyncio
import aiohttp
from aiohttp import ClientSession


class AsyncBalanceChecker:
    """Check cryptocurrency balances asynchronously across different networks."""

    def __init__(self, tron_api_url: list[str], logger: logging.Logger = None) -> None:
        """
        Initialize the AsyncBalanceChecker.

        Args:
            tron_api_url (str): The URL for the Tron API.
            logger (logging.Logger, optional): Logger for output. Defaults to None.
        """
        self.tron_api_url = tron_api_url
        self.logger = logger or logging.getLogger(__name__)
        self.api_key_index = 0
        self.session = None

    async def initialize_session(self) -> None:
        """Initialize the aiohttp ClientSession."""
        if not self.session:
            self.session = aiohttp.ClientSession()

    async def close_session(self) -> None:
        """Close the aiohttp ClientSession."""
        if self.session:
            await self.session.close()
            self.session = None

    def get_url(self, address: str) -> str:
        """
        Get the API URL for a given network.
        
        Args:
            address (str): The wallet address to check.
            
        Returns:
            str: The formatted API URL.
        """
        return f"https://apilist.tronscanapi.com/api/account/tokens?address={address}&start=0&limit=100&token=&hidden=0&show=0&sortType=0&sortBy=0"

    async def fetch(self, session: ClientSession, url: str, headers: dict = None, 
                   timeout: int = 10, max_retry: int = 3) -> dict:
        """
        Fetch balance from a given API endpoint asynchronously.
        
        Args:
            session (ClientSession): The aiohttp session.
            url (str): The API endpoint URL.
            headers (dict, optional): Request headers. Defaults to None.
            timeout (int, optional): Request timeout in seconds. Defaults to 10.
            max_retry (int, optional): Maximum retry attempts. Defaults to 3.
            
        Returns:
            dict: The API response data.
        """
        try:
            async with session.get(url, timeout=timeout, headers=headers) as response:
                if response.status == 200:
                    return await response.json()

                text_response = await response.text()

                if response.status == 429:
                    self.logger.warning("Rate limit exceeded. Waiting for 1 second...")
                    self.logger.warning("Remaining retries: %s", max_retry)

                    if max_retry < 0:
                        return None

                    await asyncio.sleep(1)
                    max_retry -= 1
                    return await self.fetch(session, url, timeout=timeout, max_retry=max_retry)

                if response.status == 403:
                    self.logger.error(
                        "API key error. Please check your API key. Response: %s", text_response)
                    return None

                if response.status == 404:
                    self.logger.error(
                        "API endpoint not found. Please check the URL. Response: %s", text_response)
                    return None

                if response.status == 500:
                    self.logger.error(
                        "Internal server error. Please try again later. Response: %s", text_response)
                    return None

                self.logger.error(
                    "Unknown error. Status: %s, Response: %s", response.status, text_response)
                return None

        except asyncio.TimeoutError:
            self.logger.error("Request timed out for URL: %s", url)
            return None
        except Exception as e:
            self.logger.error("Error fetching data: %s", str(e))
            return None

    async def check_balance(self, wallet: dict) -> dict:
        """
        Check balance for a single wallet.
        
        Args:
            wallet (dict): Wallet information including addresses.
            
        Returns:
            dict: Wallet information with balance data.
        """
        try:
            url = self.get_url(wallet['tron'])
            headers = {"TRON-PRO-API-KEY": self.tron_api_url}
            result = await self.fetch(self.session, url, headers=headers)

            if result:
                wallet['balances'] = {
                    'tron': float(result.get('total', 0))
                }
            else:
                wallet['balances'] = {'tron': 0.0}

            return wallet

        except Exception as e:
            self.logger.error("Error checking balance: %s", str(e))
            wallet['balances'] = {'tron': 0.0}
            return wallet

    async def check_alls(self, wallets: list[dict], batch_size: int = 25) -> list[dict]:
        """
        Check balances for multiple wallets in batches.
        
        Args:
            wallets (list[dict]): List of wallet information.
            batch_size (int, optional): Number of concurrent requests. Defaults to 25.
            
        Returns:
            list[dict]: List of wallets with balance information.
        """
        try:
            await self.initialize_session()
            results = []
            
            for i in range(0, len(wallets), batch_size):
                batch = wallets[i:i + batch_size]
                tasks = [self.check_balance(wallet) for wallet in batch]
                batch_results = await asyncio.gather(*tasks)
                results.extend(batch_results)
            
            return results
        
        finally:
            await self.close_session()

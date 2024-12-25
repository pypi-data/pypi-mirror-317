# CryptoBalanceFinder

A Python package for finding cryptocurrency wallet balances across multiple blockchain networks.

## Features

- Check wallet balances across multiple blockchain networks
- Asynchronous balance checking for improved performance
- Support for wallet generation from seed phrases
- Configurable batch processing
- Detailed logging and error handling

## Installation

```bash
pip install cryptobalancefinder
```

## Quick Start

```python
import asyncio
from cryptobalancefinder import WalletManager

# Initialize the wallet manager
wallet_manager = WalletManager(config_path="config.yml", batch_size=25)

# Generate wallet from seed phrase
seed_phrase = "your twelve word seed phrase here"
wallet = wallet_manager.get_wallet(seed_phrase)

# Check balances
async def main():
    await wallet_manager.check_balance([wallet])

asyncio.run(main())
```

## Configuration

Create a `config.yml` file with your API keys:

```yaml
api_keys:
  tron_grid:
    - 'your-tron-grid-api-key'
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

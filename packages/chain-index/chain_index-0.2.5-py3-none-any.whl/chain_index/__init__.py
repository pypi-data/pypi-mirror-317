from .core import (
    get_chain_info, 
    ChainInfo, 
    TokenInfo, 
    ChainTokens, 
    get_token_info, 
    get_chain_tokens, 
    get_all_chain_tokens
)
from .exceptions import ChainNotFoundError, TokenNotFoundError

__all__ = [
    "get_chain_info",
    "get_token_info",
    "get_chain_tokens",
    "get_all_chain_tokens",
    "ChainInfo",
    "TokenInfo",
    "ChainTokens",
    "ChainNotFoundError",
    "TokenNotFoundError"
]

__version__ = '0.1.8'
__author__ = 'gmatrix'
__license__ = 'MIT'

__doc__ = """
Chain Index is a Python package for retrieving information about blockchain networks.

It provides easy access to details such as native currencies, RPC URLs, common tokens,
and more for various chains. The package supports querying by chain ID, name, or alias,
and includes robust error handling.

Quick example:
    from chain_index import get_chain_info, get_token_info, ChainNotFoundError, TokenNotFoundError

    try:
        # Get chain info
        ethereum = get_chain_info(1)
        print(f"Ethereum native currency: {ethereum.nativeCurrency.symbol}")

        # Get token info
        usdt = get_token_info(1, "USDT")
        print(f"USDT contract on Ethereum: {usdt.contract}")
    except (ChainNotFoundError, TokenNotFoundError) as e:
        print(f"Error: {e}")

For more information, visit: https://github.com/gmatrixuniverse/chain-index
"""

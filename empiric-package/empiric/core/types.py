from enum import Enum

from typing_extensions import Literal

ADDRESS = int
HEX_STR = str

# Network Types
STAGING = "staging"
TESTNET = "testnet"
INTEGRATION = "https://external.integration.starknet.io"
MAINNET = "mainnet"

Network = Literal[
    "staging", "testnet", "https://external.integration.starknet.io", "mainnet"
]


class AggregationMode(Enum):
    MEDIAN = 120282243752302  # str_to_felt("median")

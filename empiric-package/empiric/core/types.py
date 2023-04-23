from enum import IntEnum, unique
from typing import List, Literal

from empiric.core.utils import str_to_felt

ADDRESS = int
HEX_STR = str

# Network Types
STAGING = "staging"
TESTNET = "testnet"
INTEGRATION = "integration"
MAINNET = "mainnet"
SCROLL_TESTNET = "scroll_testnet"
LINEA_TESTNET = "linea_testnet"
ERA_TESTNET = "era_testnet"

Network = Literal["staging", "testnet", "integration", "mainnet"]

CHAIN_IDS = {
    INTEGRATION: 1536727068981429685321,
    TESTNET: 1536727068981429685321,
    MAINNET: 23448594291968334,
    SCROLL_TESTNET: 534353,
    LINEA_TESTNET: 59140,
    ERA_TESTNET: 280
}

GATEWAY_URLS = {
    TESTNET: "https://alpha4.starknet.io",
    INTEGRATION: "https://external.integration.starknet.io",
    MAINNET: "https://alpha-mainnet.starknet.io",
    SCROLL_TESTNET: "https://scroll-alphanet.public.blastapi.io",
    LINEA_TESTNET: "https://consensys-zkevm-goerli-prealpha.infura.io/v3/ef9b71db32e242f39c6cf0691c8b521a",
    ERA_TESTNET: "https://testnet.era.zksync.dev"
}


# aggregation mode enum
@unique
class AggregationMode(IntEnum):
    MEDIAN = 84959893733710  # str_to_felt("MEDIAN")


class Currency:
    id: int
    decimals: int
    is_abstract_currency: int
    starknet_address: int
    ethereum_address: int

    def __init__(
        self,
        id,
        decimals,
        is_abstract_currency,
        starknet_address=None,
        ethereum_address=None,
    ):
        if type(id) == str:
            id = str_to_felt(id)
        self.id = id

        self.decimals = decimals

        if type(is_abstract_currency) == bool:
            is_abstract_currency = int(is_abstract_currency)
        self.is_abstract_currency = is_abstract_currency

        if starknet_address is None:
            starknet_address = 0
        self.starknet_address = starknet_address

        if ethereum_address is None:
            ethereum_address = 0
        self.ethereum_address = ethereum_address

    def serialize(self) -> List[str]:
        return [
            self.id,
            self.decimals,
            self.is_abstract_currency,
            self.starknet_address,
            self.ethereum_address,
        ]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "decimals": self.decimals,
            "is_abstract_currency": self.is_abstract_currency,
            "starknet_address": self.starknet_address,
            "ethereum_address": self.ethereum_address,
        }


class Pair:
    id: int
    quote_currency_id: int
    base_currency_id: int

    def __init__(self, id, quote_currency_id, base_currency_id):
        if type(id) == str:
            id = str_to_felt(id)
        self.id = id

        if type(quote_currency_id) == str:
            quote_currency_id = str_to_felt(quote_currency_id)
        self.quote_currency_id = quote_currency_id

        if type(base_currency_id) == str:
            base_currency_id = str_to_felt(base_currency_id)
        self.base_currency_id = base_currency_id

    def serialize(self) -> List[str]:
        return [self.id, self.quote_currency_id, self.base_currency_id]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "quote_currency_id": self.quote_currency_id,
            "base_currency_id": self.base_currency_id,
        }

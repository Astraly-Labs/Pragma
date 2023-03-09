import os
import time
from typing import List

from empiric.core.entry import SpotEntry
from web3 import HTTPProvider, Web3

ORACLE_ADDRESS = "0x26a7756c4aC33379621Da862308f8527FED3Dc47"  # "0xc09d042ed2f47297d1e8f010aF03d6f094433D65"
ORACLE_ABI = [
    {"inputs": [], "stateMutability": "nonpayable", "type": "constructor"},
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "uint64", "name": "timestamp", "type": "uint64"},
                    {"internalType": "uint128", "name": "value", "type": "uint128"},
                    {
                        "internalType": "enum IOracle.AggregationMode",
                        "name": "aggregationMode",
                        "type": "uint8",
                    },
                    {
                        "internalType": "uint8",
                        "name": "numSourcesAggregated",
                        "type": "uint8",
                    },
                ],
                "indexed": False,
                "internalType": "struct IOracle.Checkpoint",
                "name": "cp",
                "type": "tuple",
            }
        ],
        "name": "CheckpointSpotEntry",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint8",
                "name": "version",
                "type": "uint8",
            }
        ],
        "name": "Initialized",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "previousOwner",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "newOwner",
                "type": "address",
            },
        ],
        "name": "OwnershipTransferred",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "components": [
                    {"internalType": "bytes32", "name": "id", "type": "bytes32"},
                    {"internalType": "uint256", "name": "decimals", "type": "uint256"},
                    {
                        "internalType": "bool",
                        "name": "isAbstractCurrency",
                        "type": "bool",
                    },
                    {
                        "internalType": "address",
                        "name": "ethereumAddress",
                        "type": "address",
                    },
                ],
                "indexed": False,
                "internalType": "struct ICurrencyManager.Currency",
                "name": "currency",
                "type": "tuple",
            }
        ],
        "name": "SubmittedCurrency",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "components": [
                    {"internalType": "bytes32", "name": "id", "type": "bytes32"},
                    {
                        "internalType": "bytes32",
                        "name": "quoteCurrencyId",
                        "type": "bytes32",
                    },
                    {
                        "internalType": "bytes32",
                        "name": "baseCurrencyId",
                        "type": "bytes32",
                    },
                ],
                "indexed": False,
                "internalType": "struct ICurrencyManager.Pair",
                "name": "pair",
                "type": "tuple",
            }
        ],
        "name": "SubmittedPair",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "components": [
                    {
                        "components": [
                            {
                                "internalType": "uint256",
                                "name": "timestamp",
                                "type": "uint256",
                            },
                            {
                                "internalType": "bytes32",
                                "name": "source",
                                "type": "bytes32",
                            },
                            {
                                "internalType": "bytes32",
                                "name": "publisher",
                                "type": "bytes32",
                            },
                        ],
                        "internalType": "struct IOracle.BaseEntry",
                        "name": "base",
                        "type": "tuple",
                    },
                    {"internalType": "bytes32", "name": "pairId", "type": "bytes32"},
                    {"internalType": "uint256", "name": "price", "type": "uint256"},
                    {"internalType": "uint256", "name": "volume", "type": "uint256"},
                ],
                "indexed": False,
                "internalType": "struct IOracle.SpotEntry",
                "name": "newEntry",
                "type": "tuple",
            }
        ],
        "name": "SubmittedSpotEntry",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "components": [
                    {"internalType": "bytes32", "name": "id", "type": "bytes32"},
                    {"internalType": "uint256", "name": "decimals", "type": "uint256"},
                    {
                        "internalType": "bool",
                        "name": "isAbstractCurrency",
                        "type": "bool",
                    },
                    {
                        "internalType": "address",
                        "name": "ethereumAddress",
                        "type": "address",
                    },
                ],
                "indexed": False,
                "internalType": "struct ICurrencyManager.Currency",
                "name": "currency",
                "type": "tuple",
            }
        ],
        "name": "UpdatedCurrency",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "oldPublisherRegistryAddress",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "newPublisherRegistryAddress",
                "type": "address",
            },
        ],
        "name": "UpdatedPublisherRegistryAddress",
        "type": "event",
    },
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "bytes32", "name": "id", "type": "bytes32"},
                    {"internalType": "uint256", "name": "decimals", "type": "uint256"},
                    {
                        "internalType": "bool",
                        "name": "isAbstractCurrency",
                        "type": "bool",
                    },
                    {
                        "internalType": "address",
                        "name": "ethereumAddress",
                        "type": "address",
                    },
                ],
                "internalType": "struct ICurrencyManager.Currency",
                "name": "currency",
                "type": "tuple",
            }
        ],
        "name": "addCurrency",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "bytes32", "name": "id", "type": "bytes32"},
                    {
                        "internalType": "bytes32",
                        "name": "quoteCurrencyId",
                        "type": "bytes32",
                    },
                    {
                        "internalType": "bytes32",
                        "name": "baseCurrencyId",
                        "type": "bytes32",
                    },
                ],
                "internalType": "struct ICurrencyManager.Pair",
                "name": "pair",
                "type": "tuple",
            }
        ],
        "name": "addPair",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "name": "checkpointIndex",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "bytes32", "name": "", "type": "bytes32"},
            {"internalType": "uint256", "name": "", "type": "uint256"},
        ],
        "name": "checkpoints",
        "outputs": [
            {"internalType": "uint64", "name": "timestamp", "type": "uint64"},
            {"internalType": "uint128", "name": "value", "type": "uint128"},
            {
                "internalType": "enum IOracle.AggregationMode",
                "name": "aggregationMode",
                "type": "uint8",
            },
            {"internalType": "uint8", "name": "numSourcesAggregated", "type": "uint8"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "name": "currencies",
        "outputs": [
            {"internalType": "bytes32", "name": "id", "type": "bytes32"},
            {"internalType": "uint256", "name": "decimals", "type": "uint256"},
            {"internalType": "bool", "name": "isAbstractCurrency", "type": "bool"},
            {"internalType": "address", "name": "ethereumAddress", "type": "address"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "bytes32", "name": "", "type": "bytes32"},
            {"internalType": "uint256", "name": "", "type": "uint256"},
        ],
        "name": "oracleSourcesStorage",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "bytes32", "name": "", "type": "bytes32"},
            {"internalType": "bytes32", "name": "", "type": "bytes32"},
        ],
        "name": "pairIdStorage",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "name": "pairs",
        "outputs": [
            {"internalType": "bytes32", "name": "id", "type": "bytes32"},
            {"internalType": "bytes32", "name": "quoteCurrencyId", "type": "bytes32"},
            {"internalType": "bytes32", "name": "baseCurrencyId", "type": "bytes32"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "publisherRegistry",
        "outputs": [
            {
                "internalType": "contract IPublisherRegistry",
                "name": "",
                "type": "address",
            }
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "renounceOwnership",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "bytes32", "name": "", "type": "bytes32"},
            {"internalType": "bytes32", "name": "", "type": "bytes32"},
        ],
        "name": "spotEntryStorage",
        "outputs": [
            {"internalType": "uint128", "name": "timestamp", "type": "uint128"},
            {"internalType": "bytes16", "name": "pairId", "type": "bytes16"},
            {"internalType": "uint128", "name": "price", "type": "uint128"},
            {"internalType": "uint128", "name": "volume", "type": "uint128"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "newOwner", "type": "address"}],
        "name": "transferOwnership",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "bytes32", "name": "id", "type": "bytes32"},
                    {"internalType": "uint256", "name": "decimals", "type": "uint256"},
                    {
                        "internalType": "bool",
                        "name": "isAbstractCurrency",
                        "type": "bool",
                    },
                    {
                        "internalType": "address",
                        "name": "ethereumAddress",
                        "type": "address",
                    },
                ],
                "internalType": "struct ICurrencyManager.Currency",
                "name": "currency",
                "type": "tuple",
            }
        ],
        "name": "updateCurrency",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_publisherRegistry",
                "type": "address",
            },
            {
                "components": [
                    {"internalType": "bytes32", "name": "id", "type": "bytes32"},
                    {"internalType": "uint256", "name": "decimals", "type": "uint256"},
                    {
                        "internalType": "bool",
                        "name": "isAbstractCurrency",
                        "type": "bool",
                    },
                    {
                        "internalType": "address",
                        "name": "ethereumAddress",
                        "type": "address",
                    },
                ],
                "internalType": "struct ICurrencyManager.Currency[]",
                "name": "_currencies",
                "type": "tuple[]",
            },
            {
                "components": [
                    {"internalType": "bytes32", "name": "id", "type": "bytes32"},
                    {
                        "internalType": "bytes32",
                        "name": "quoteCurrencyId",
                        "type": "bytes32",
                    },
                    {
                        "internalType": "bytes32",
                        "name": "baseCurrencyId",
                        "type": "bytes32",
                    },
                ],
                "internalType": "struct ICurrencyManager.Pair[]",
                "name": "_pairs",
                "type": "tuple[]",
            },
        ],
        "name": "initialize",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "threshold", "type": "uint256"}],
        "name": "setSourcesThreshold",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {
                "internalType": "contract IPublisherRegistry",
                "name": "newPublisherRegistryAddress",
                "type": "address",
            }
        ],
        "name": "updatePublisherRegistryAddress",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "components": [
                            {
                                "internalType": "uint256",
                                "name": "timestamp",
                                "type": "uint256",
                            },
                            {
                                "internalType": "bytes32",
                                "name": "source",
                                "type": "bytes32",
                            },
                            {
                                "internalType": "bytes32",
                                "name": "publisher",
                                "type": "bytes32",
                            },
                        ],
                        "internalType": "struct IOracle.BaseEntry",
                        "name": "base",
                        "type": "tuple",
                    },
                    {"internalType": "bytes32", "name": "pairId", "type": "bytes32"},
                    {"internalType": "uint256", "name": "price", "type": "uint256"},
                    {"internalType": "uint256", "name": "volume", "type": "uint256"},
                ],
                "internalType": "struct IOracle.SpotEntry",
                "name": "spotEntry",
                "type": "tuple",
            }
        ],
        "name": "publishSpotEntry",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "bytes32", "name": "pairId", "type": "bytes32"},
            {
                "internalType": "enum IOracle.AggregationMode",
                "name": "aggregationMode",
                "type": "uint8",
            },
        ],
        "name": "setCheckpoint",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "bytes32[]", "name": "pairIds", "type": "bytes32[]"},
            {
                "internalType": "enum IOracle.AggregationMode",
                "name": "aggregationMode",
                "type": "uint8",
            },
        ],
        "name": "setCheckpoints",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "components": [
                            {
                                "internalType": "uint256",
                                "name": "timestamp",
                                "type": "uint256",
                            },
                            {
                                "internalType": "bytes32",
                                "name": "source",
                                "type": "bytes32",
                            },
                            {
                                "internalType": "bytes32",
                                "name": "publisher",
                                "type": "bytes32",
                            },
                        ],
                        "internalType": "struct IOracle.BaseEntry",
                        "name": "base",
                        "type": "tuple",
                    },
                    {"internalType": "bytes32", "name": "pairId", "type": "bytes32"},
                    {"internalType": "uint256", "name": "price", "type": "uint256"},
                    {"internalType": "uint256", "name": "volume", "type": "uint256"},
                ],
                "internalType": "struct IOracle.SpotEntry[]",
                "name": "spotEntries",
                "type": "tuple[]",
            }
        ],
        "name": "publishSpotEntries",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "bytes32", "name": "pairId", "type": "bytes32"},
            {
                "internalType": "enum IOracle.AggregationMode",
                "name": "",
                "type": "uint8",
            },
            {"internalType": "bytes32[]", "name": "sources", "type": "bytes32[]"},
        ],
        "name": "getSpot",
        "outputs": [
            {"internalType": "uint256", "name": "price", "type": "uint256"},
            {"internalType": "uint256", "name": "decimals", "type": "uint256"},
            {
                "internalType": "uint256",
                "name": "lastUpdatedTimestamp",
                "type": "uint256",
            },
            {
                "internalType": "uint256",
                "name": "numSourcesAggregated",
                "type": "uint256",
            },
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "bytes32", "name": "pairId", "type": "bytes32"},
            {"internalType": "bytes32[]", "name": "sources", "type": "bytes32[]"},
        ],
        "name": "getSpotEntries",
        "outputs": [
            {
                "components": [
                    {"internalType": "uint128", "name": "timestamp", "type": "uint128"},
                    {"internalType": "bytes16", "name": "pairId", "type": "bytes16"},
                    {"internalType": "uint128", "name": "price", "type": "uint128"},
                    {"internalType": "uint128", "name": "volume", "type": "uint128"},
                ],
                "internalType": "struct IOracle.SpotEntryStorage[]",
                "name": "entries",
                "type": "tuple[]",
            },
            {
                "internalType": "uint256",
                "name": "lastUpdatedTimestamp",
                "type": "uint256",
            },
        ],
        "stateMutability": "view",
        "type": "function",
    },
]


class EvmHelper:
    def __init__(
        self,
        publisher,
        sender_address,
        private_key,
        provider_uri=,  # "https://zksync2-testnet.zksync.dev",
    ):
        self.w3 = Web3(HTTPProvider(endpoint_uri=provider_uri))
        self.chain_id = 59140  # Consensys ZkEVM testnet chain id
        self.oracle = self.w3.eth.contract(
            address=ORACLE_ADDRESS,
            abi=ORACLE_ABI,
        )
        self.publisher = publisher
        self.sender = sender_address or os.environ["SENDER_ADDRESS"]
        self.private_key = private_key or os.environ["PRIVATE_KEY"]

    def publish_spot_entry(
        self,
        pair,
        price,
        source,
        volume=0,
        gas_price=int(1e8),
    ):
        nonce = self.w3.eth.getTransactionCount(self.sender)
        txn = self.oracle.functions.publishSpotEntry(
            {
                "base": {
                    "timestamp": int(time.time()),
                    "source": source,
                    "publisher": self.publisher,
                },
                "pairId": b"ETH/USD",
                "price": price,
                "volume": volume,
            }
        ).buildTransaction(
            {
                "nonce": nonce,
                "gasPrice": gas_price,
                "chainId": self.chain_id,
                "from": self.sender,
            }
        )
        print(txn)
        signed_txn = self.w3.eth.account.signTransaction(
            txn, private_key=self.private_key
        )
        self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)

        return signed_txn.hash.hex()

    def publish_spot_entries(self, spot_entries: List[SpotEntry], gas_price=int(1e8)):
        print(spot_entries)
        serialized_spot_entries = SpotEntry.serialize_entries_evm(spot_entries)
        print(serialized_spot_entries)
        nonce = self.w3.eth.get_transaction_count(self.sender)
        print("nonce", nonce)
        print(self.oracle.functions)
        print(self.oracle.functions.publishSpotEntries)
        txn = self.oracle.functions.publishSpotEntries(
            {"spotEntries": serialized_spot_entries}
        ).build_transaction(
            {
                "nonce": nonce,
                "chainId": 59140,
                "from": self.sender,
            }
        )
        print(txn)
        signed_txn = self.w3.eth.account.sign_transaction(
            txn, private_key=self.private_key
        )
        print(signed_txn)
        hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        return hash.hex()

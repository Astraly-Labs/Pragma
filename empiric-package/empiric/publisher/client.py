from typing import Optional

from empiric.core import LOGGER
from empiric.core.base_client import EmpiricAccountClient, EmpiricBaseClient
from empiric.core.config import CONFIG
from empiric.core.entry import serialize_entries, serialize_entry
from empiric.core.types import ADDRESS, HEX_STR, TESTNET, Network


class EmpiricPublisherClient(EmpiricBaseClient):
    publisher: Optional[ADDRESS]
    publisher_registry_address: Optional[ADDRESS]
    account_client: EmpiricAccountClient

    def __init__(
        self,
        publisher_private_key,
        publisher_address,
        publisher: Optional[ADDRESS] = None,
        publisher_registry_address: Optional[ADDRESS] = None,
        network: Network = TESTNET,
        oracle_controller_address: Optional[ADDRESS] = None,
    ):
        self.publisher_registry_address = (
            publisher_registry_address
            if publisher_registry_address is not None
            else CONFIG[network].PUBLISHER_REGISTRY_ADDRESS
        )
        self.publisher = publisher
        super().__init__(
            publisher_private_key,
            publisher_address,
            network,
            oracle_controller_address,
        )
        # Override default account_client with one that uses timestamp for nonce
        self.account_client = EmpiricAccountClient(
            self.account_contract_address, self.client, self.signer
        )

    async def _fetch_contracts(self):
        await self._fetch_base_contracts()

    async def update_publisher_address(self, new_address, publisher=None) -> HEX_STR:
        publisher = publisher or self.publisher
        if publisher is None:
            raise ValueError(
                "No publisher provided at method call or instantiation, but need publisher ID to update address"
            )

        result = await self.send_transaction(
            self.publisher_registry_address,
            "update_publisher_address",
            [publisher, new_address],
        )
        LOGGER.info(f"Updated publisher address with transaction {result}")

        return result

    async def publish(self, entry) -> HEX_STR:
        result = await self.send_transaction(
            self.oracle_controller_address,
            "publish_entry",
            serialize_entry(entry),
        )
        LOGGER.info(f"Updated entry with transaction {result}")

        return result

    async def publish_many(self, entries) -> HEX_STR:
        if len(entries) == 0:
            LOGGER.warn("Skipping publishing as entries array is empty")
            return

        result = await self.send_transaction(
            self.oracle_controller_address,
            "publish_entries",
            serialize_entries(entries),
        )

        LOGGER.info(
            f"Successfully sent {len(entries)} updated entries with transaction {result}"
        )

        return result

from typing import List

from empiric.core.contract import Contract
from empiric.core.utils import str_to_felt
from starknet_py.contract import InvokeResult
from starknet_py.net.client import Client


class PublisherRegistryMixin:
    client: Client
    publisher_registry: Contract

    async def get_all_publishers(self) -> List[str]:
        result = await self.publisher_registry.get_all_publishers.call()
        return result.publishers

    async def get_publisher_address(self, publisher) -> str:
        result = await self.publisher_registry.get_publisher_address.call(publisher)
        return result.publisher_address

    async def register_publisher(
        self, publisher: str, publisher_address: int, max_fee=int(1e16), auto_estimate: bool = False
    ) -> InvokeResult:
        invocation = await self.publisher_registry.register_publisher.invoke(
            str_to_felt(publisher),
            publisher_address,
            max_fee=max_fee,
            auto_estimate=auto_estimate,
        )
        return invocation

    async def update_publisher_address(
        self, publisher_address: int, publisher: str, max_fee=int(1e16), auto_estimate: bool = False
    ) -> InvokeResult:
        invocation = await self.publisher_registry.update_publisher_address.invoke(
            str_to_felt(publisher),
            publisher_address,
            max_fee=max_fee,
            auto_estimate=auto_estimate,
        )
        return invocation

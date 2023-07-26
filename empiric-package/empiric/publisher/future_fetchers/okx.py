import logging
from typing import List, Union

import requests
from aiohttp import ClientSession
from empiric.core.entry import FutureEntry
from empiric.core.utils import currency_pair_to_pair_id
from empiric.publisher.assets import EmpiricAsset, EmpiricFutureAsset
from empiric.publisher.types import PublisherFetchError, PublisherInterfaceT

logger = logging.getLogger(__name__)


class OkxFutureFetcher(PublisherInterfaceT):
    BASE_URL: str = "https://okx.com/api/v5/market/ticker"
    SOURCE: str = "OKX"
    TIMESTAMP_URL: str = "https://www.okx.com/api/v5/public/instruments"
    publisher: str

    def __init__(self, assets: List[EmpiricAsset], publisher):
        self.assets = assets
        self.publisher = publisher

    async def fetch_expiry_timestamp( self,asset,id,session):
        pair = asset["pair"]
        url = f"{self.TIMESTAMP_URL}?instType=FUTURES&instId={id}"
        async with session.get(url) as resp:
            if resp.status == 404:
                return PublisherFetchError(
                    f"No data found for {'/'.join(pair)} from OKX"
                )
            result = await resp.json(content_type="application/json")
            if (
                result["code"] == "51001"
                or result["msg"] == "Instrument ID does not exist"
            ):
                return PublisherFetchError(
                    f"No data found for {'/'.join(pair)} from OKX"
                )
            return result["data"][0]["expTime"]

    async def construct_future_entry(self,asset, result, publisher, session):
        result_arr = []
        result_len = len(result["data"])
        pair = asset["pair"]
        for i in range(0,result_len):
            data = result["data"][i]
            timestamp = int(data["ts"])
            price = float(data["last"])
            price_int = int(price * (10 ** asset["decimals"]))
            pair_id = currency_pair_to_pair_id(*pair)
            volume = float(data["volCcy24h"])
            volume_int = int(volume)
            expiry_timestamp = await self.fetch_expiry_timestamp(asset, data["instId"], session)
            result_arr.append(FutureEntry(
            pair_id=pair_id,
            price=price_int,
            volume=volume_int,
            timestamp=timestamp,
            source=self.SOURCE,
            publisher=publisher,
            expiry_timestamp=expiry_timestamp,
        ))
        logger.info(f"Fetched future for {'/'.join(pair)} from OKX")

        return result_arr
    async def fetch_future_pair(self,asset, session, publisher):
        pair = asset["pair"]
        url = f"{self.BASE_URL}?instType=FUTURES&uly={pair[0]}-{pair[1]}"

        async with session.get(url) as resp:
            if resp.status == 404:
                return PublisherFetchError(
                    f"No data found for {'/'.join(pair)} from OKX"
                )
            result = await resp.json(content_type="application/json")
            if (
                result["code"] == "51001"
                or result["msg"] == "Instrument ID does not exist"
            ):
                return PublisherFetchError(
                    f"No data found for {'/'.join(pair)} from OKX"
                )
            return await self.construct_future_entry(asset, result, publisher, session)
    async def fetch_futures(self,assets, session, publisher):
        entries = []
        for asset in assets:
            if asset["type"] != "FUTURE":
                logger.debug(f"Skipping OKX for non-future asset {asset}")
                continue
            future_entries = await self.fetch_future_pair(asset, session, publisher)
            if isinstance(future_entries, list):
                entries.extend(future_entries)
            else:
                entries.append(future_entries)
        return entries


    def print_future_entry(entry):
        print(f"Pair ID: {entry.pair_id}")
        print(f"Price: {entry.price}")
        print(f"Volume: {entry.volume}")
        print(f"Timestamp: {entry.base.timestamp}")
        print(f"Source: {entry.base.source}")
        print(f"Publisher: {entry.base.publisher}")
        print(f"Expiry timestamp: {entry.expiry_timestamp}")
        print("---")

    def print_futures(self,entries):
        for entry in entries:
            if isinstance(entry, PublisherFetchError):
                print(f"Error fetching future: {entry}")
            else:
                self.print_future_entry(entry)






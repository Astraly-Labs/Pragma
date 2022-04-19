import os
from statistics import median

import pytest
import pytest_asyncio
from pontis.core.entry import Entry
from pontis.core.utils import (
    sign_entry,
    sign_publisher,
    sign_publisher_registration,
    str_to_felt,
)
from starkware.crypto.signature.signature import (
    get_random_private_key,
    private_to_stark_key,
    sign,
)
from starkware.starknet.testing.starknet import Starknet
from starkware.starkware_utils.error_handling import StarkException

# The path to the contract source code.
CONTRACT_FILE = os.path.join(os.path.dirname(__file__), "../contracts/Oracle.cairo")


@pytest_asyncio.fixture
async def contract(private_and_public_registration_keys):
    _, registration_public_key = private_and_public_registration_keys

    starknet = await Starknet.empty()
    contract = await starknet.deploy(
        source=CONTRACT_FILE, constructor_calldata=[registration_public_key]
    )

    return contract


@pytest_asyncio.fixture
async def registered_contract(
    contract,
    private_and_public_publisher_keys,
    private_and_public_registration_keys,
    publisher,
):
    publisher_private_key, publisher_public_key = private_and_public_publisher_keys
    publisher_signature_r, publisher_signature_s = sign_publisher(
        publisher, publisher_private_key
    )

    registration_private_key, _ = private_and_public_registration_keys
    registration_signature_r, registration_signature_s = sign_publisher_registration(
        publisher_public_key, publisher, registration_private_key
    )

    await contract.register_publisher(
        publisher_public_key,
        publisher,
        publisher_signature_r,
        publisher_signature_s,
        registration_signature_r,
        registration_signature_s,
    ).invoke()

    return contract


@pytest.mark.asyncio
async def test_deploy(contract):
    return


@pytest.mark.asyncio
async def test_publish(
    registered_contract, private_and_public_publisher_keys, publisher
):
    private_key, _ = private_and_public_publisher_keys
    entry = Entry(key=str_to_felt("usd/eth"), value=2, timestamp=1, publisher=publisher)

    signature_r, signature_s = sign_entry(entry, private_key)

    await registered_contract.submit_entry(entry, signature_r, signature_s).invoke()

    result = await registered_contract.get_value(entry.key).invoke()
    assert result.result.value == entry.value

    return


@pytest.mark.asyncio
async def test_republish(
    registered_contract, private_and_public_publisher_keys, publisher
):
    private_key, _ = private_and_public_publisher_keys
    key = str_to_felt("usd/eth")
    entry = Entry(key=key, value=2, timestamp=1, publisher=publisher)

    signature_r, signature_s = sign_entry(entry, private_key)

    await registered_contract.submit_entry(entry, signature_r, signature_s).invoke()

    result = await registered_contract.get_value(entry.key).invoke()
    assert result.result.value == entry.value

    second_entry = entry = Entry(key=key, value=3, timestamp=2, publisher=publisher)

    signature_r, signature_s = sign_entry(second_entry, private_key)

    await registered_contract.submit_entry(
        second_entry, signature_r, signature_s
    ).invoke()

    result = await registered_contract.get_value(second_entry.key).invoke()
    assert result.result.value == second_entry.value

    return


@pytest.mark.asyncio
async def test_republish_stale(
    registered_contract, private_and_public_publisher_keys, publisher
):
    private_key, _ = private_and_public_publisher_keys
    key = str_to_felt("usd/eth")
    entry = Entry(key=key, value=2, timestamp=2, publisher=publisher)

    signature_r, signature_s = sign_entry(entry, private_key)

    await registered_contract.submit_entry(entry, signature_r, signature_s).invoke()

    result = await registered_contract.get_value(entry.key).invoke()
    assert result.result.value == entry.value

    second_entry = Entry(key=key, value=3, timestamp=1, publisher=publisher)

    signature_r, signature_s = sign_entry(second_entry, private_key)

    try:
        await registered_contract.submit_entry(
            second_entry, signature_r, signature_s
        ).invoke()

        raise Exception(
            "Transaction to submit stale price succeeded, but should not have."
        )
    except StarkException:
        pass

    result = await registered_contract.get_value(second_entry.key).invoke()
    assert result.result.value == entry.value

    return


@pytest.mark.asyncio
async def test_publish_second_asset(
    registered_contract, private_and_public_publisher_keys, publisher
):
    private_key, _ = private_and_public_publisher_keys
    entry = Entry(key=str_to_felt("usd/eth"), value=2, timestamp=1, publisher=publisher)

    signature_r, signature_s = sign_entry(entry, private_key)

    await registered_contract.submit_entry(entry, signature_r, signature_s).invoke()

    result = await registered_contract.get_value(entry.key).invoke()
    assert result.result.value == entry.value

    second_entry = Entry(
        key=str_to_felt("usd/btc"), value=2, timestamp=1, publisher=publisher
    )

    signature_r, signature_s = sign_entry(second_entry, private_key)

    await registered_contract.submit_entry(
        second_entry, signature_r, signature_s
    ).invoke()

    result = await registered_contract.get_value(second_entry.key).invoke()
    assert result.result.value == second_entry.value

    # Check that first asset is still stored accurately
    result = await registered_contract.get_value(entry.key).invoke()
    assert result.result.value == entry.value

    return


@pytest.mark.asyncio
async def test_publish_second_publisher(
    registered_contract,
    private_and_public_publisher_keys,
    private_and_public_registration_keys,
    publisher,
):
    key = str_to_felt("usd/eth")
    private_key, _ = private_and_public_publisher_keys
    entry = Entry(key=key, value=3, timestamp=1, publisher=publisher)
    signature_r, signature_s = sign_entry(entry, private_key)

    await registered_contract.submit_entry(entry, signature_r, signature_s).invoke()

    second_publisher_private_key = get_random_private_key()
    second_publisher_public_key = private_to_stark_key(second_publisher_private_key)

    second_publisher = str_to_felt("bar")
    second_publisher_signature_r, second_publisher_signature_s = sign(
        second_publisher, second_publisher_private_key
    )

    registration_private_key, _ = private_and_public_registration_keys
    registration_signature_r, registration_signature_s = sign_publisher_registration(
        second_publisher_public_key, second_publisher, registration_private_key
    )

    await registered_contract.register_publisher(
        second_publisher_public_key,
        second_publisher,
        second_publisher_signature_r,
        second_publisher_signature_s,
        registration_signature_r,
        registration_signature_s,
    ).invoke()

    second_entry = Entry(key=key, value=5, timestamp=1, publisher=second_publisher)

    signature_r, signature_s = sign_entry(second_entry, second_publisher_private_key)

    await registered_contract.submit_entry(
        second_entry, signature_r, signature_s
    ).invoke()

    result = await registered_contract.get_value(key).invoke()
    assert result.result.value == (second_entry.value + entry.value) / 2

    result = await registered_contract.get_entries_for_key(key).invoke()
    assert result.result.entries == [entry, second_entry]

    return


async def register_new_publisher_and_submit_entry(
    contract, registration_private_key, publisher, entry
):
    publisher_private_key = get_random_private_key()
    publisher_public_key = private_to_stark_key(publisher_private_key)

    publisher_signature_r, publisher_signature_s = sign(
        publisher, publisher_private_key
    )

    registration_signature_r, registration_signature_s = sign_publisher_registration(
        publisher_public_key, publisher, registration_private_key
    )

    await contract.register_publisher(
        publisher_public_key,
        publisher,
        publisher_signature_r,
        publisher_signature_s,
        registration_signature_r,
        registration_signature_s,
    ).invoke()

    signature_r, signature_s = sign_entry(entry, publisher_private_key)

    await contract.submit_entry(entry, signature_r, signature_s).invoke()

    return


@pytest.mark.asyncio
async def test_median_aggregation(
    registered_contract,
    private_and_public_publisher_keys,
    private_and_public_registration_keys,
    publisher,
):
    key = str_to_felt("usd/eth")
    prices = [1, 3, 10, 5, 12, 2]
    publishers = ["foo", "bar", "baz", "oof", "rab", "zab"]
    private_key, _ = private_and_public_publisher_keys
    entry = Entry(key=key, value=prices[0], timestamp=1, publisher=publisher)
    signature_r, signature_s = sign_entry(entry, private_key)

    await registered_contract.submit_entry(entry, signature_r, signature_s).invoke()

    entries = [entry]

    registration_private_key, _ = private_and_public_registration_keys

    for price, additional_publisher_str in zip(prices[1:], publishers[1:]):
        additional_publisher = str_to_felt(additional_publisher_str)
        additional_entry = Entry(
            key=key, value=price, timestamp=1, publisher=additional_publisher
        )
        entries.append(additional_entry)
        await register_new_publisher_and_submit_entry(
            registered_contract,
            registration_private_key,
            additional_publisher,
            additional_entry,
        )

        result = await registered_contract.get_entries_for_key(key).invoke()
        assert result.result.entries == entries

        result = await registered_contract.get_value(key).invoke()
        assert result.result.value == int(median(prices[: len(entries)]))

        print(f"Succeeded for {len(entries)} entries")

    return

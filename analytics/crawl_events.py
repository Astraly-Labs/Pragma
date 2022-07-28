import json
import requests
import os.path
import pandas as pd
from empiric.core.utils import felt_to_str


JSON_FILE = "empiric-events.json"
CSV_FILE = "empiric-events.csv"


def get_events():
    """If no JSON file in current directory, requests all events from Starknet Indexer."""
    if not os.path.isfile(JSON_FILE):
        print("Requesting all SubmittedEntry events from Starknet Indexer...")
        url = "https://starknet-archive.hasura.app/v1/graphql"
        request_json = {
            "query": 'query empiric { event(where: {name: {_eq: "SubmittedEntry"}, transmitter_contract: {_eq: "0x12fadd18ec1a23a160cc46981400160fbf4a7a5eed156c4669e39807265bcd4"}}) { name arguments { value } transaction_hash }}'
        }
        r = requests.post(url=url, json=request_json)
        data = r.json()
    else:
        print(f"Reading in {JSON_FILE}...")
        with open(JSON_FILE) as data_file:
            data = json.load(data_file)
    return data


def format_events(data):
    """Returns a list of Events. Each event's fields are converted to ints."""
    events = data["data"]["event"]
    formatted_events = [event["arguments"][0]["value"] for event in events]
    return [
        {key: int(value, 16) for key, value in event.items()}
        for event in formatted_events
    ]


def to_csv(formatted_events):
    print(f"Converting to {CSV_FILE}...")
    df = pd.DataFrame(formatted_events)
    df["key"] = df["key"].apply(felt_to_str)
    df["value"] = df["value"] / (10**18)
    df["datetime"] = pd.to_datetime(df["timestamp"], unit="s")
    df["publisher"] = df["publisher"].apply(felt_to_str)
    df["source"] = df["source"].apply(felt_to_str)
    df.to_csv(CSV_FILE)
    print(f"Found {df.shape[0]} events.")


if __name__ == "__main__":
    events = get_events()
    formatted_events = format_events(events)
    to_csv(formatted_events)

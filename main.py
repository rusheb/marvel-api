import json
from datetime import datetime
from hashlib import md5
from os import environ
from typing import Dict, Generator

import requests
import requests_cache

REQUEST_URL = "http://gateway.marvel.com/v1/public/characters"
PUBLIC_KEY = environ["MARVEL_PUBLIC_KEY"]
PRIVATE_KEY = environ["MARVEL_PRIVATE_KEY"]


def get_all_characters(offset: int = 0) -> Generator[Dict, None, None]:
    characters = None
    while characters != []:
        try:
            characters = get_characters_chunk(offset)
            for character in characters:
                yield character

            offset += 100
        except Exception:
            raise


def get_characters_chunk(offset: int) -> Dict:
    print(f"Getting characters {offset} to {offset + 100}")

    now = datetime.now().strftime("%b %d %Y %H:%M:%S")
    hash_param = md5(f"{now}{PRIVATE_KEY}{PUBLIC_KEY}".encode("utf-8")).hexdigest()

    params = {
        "apikey": PUBLIC_KEY,
        "ts": now,
        "hash": hash_param,
        "limit": "100",
        "offset": str(offset),
    }

    response_string = requests.get(REQUEST_URL, params=params)
    response_json = json.loads(response_string.content.decode("utf-8"))
    return response_json["data"]["results"]


if __name__ == "__main__":
    requests_cache.install_cache("marvel_cache", ignored_parameters=["hash", "ts"])

    ids = [character["id"] for character in get_all_characters()]

    print(f"Found {len(ids)} ids")
    print(ids)

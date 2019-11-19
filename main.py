import json
from datetime import datetime
from hashlib import md5
from os import environ

import requests
import requests_cache

URL = "http://gateway.marvel.com/v1/public/characters"
PUBLIC_KEY = environ["MARVEL_PUBLIC_KEY"]
PRIVATE_KEY = environ["MARVEL_PRIVATE_KEY"]


def get_characters(offset: int):
    print(f"Getting characters {offset} to {offset + 100}")

    now = datetime.now().strftime("%b %d %Y %H:%M:%S")
    string_to_hash = now + PRIVATE_KEY + PUBLIC_KEY
    request_hash = md5(string_to_hash.encode("utf-8")).hexdigest()

    params = {
        "apikey": PUBLIC_KEY,
        "ts": now,
        "hash": request_hash,
        "limit": "100",
        "offset": str(offset),
    }
    response_string = requests.get(URL, params=params)
    response_dict = json.loads(response_string.content.decode("utf-8"))
    try:
        return response_dict["data"]["results"]
    except Exception:
        print(response_dict)
        return


if __name__ == "__main__":
    requests_cache.install_cache("marvel_cache", ignored_parameters=["hash", "ts"])

    offset = 1300
    characters = get_characters(offset)
    ids = [character["id"] for character in characters]

    while characters != []:
        offset += 100
        characters = get_characters(offset)
        ids += [character["id"] for character in characters]

    print(f"Found {len(ids)} ids")
    print(ids)

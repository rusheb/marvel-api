import json
from datetime import datetime
from hashlib import md5
from os import environ
from pprint import pprint
from typing import Dict, Generator

import requests
from translate import Translator

BASE_URL = "http://gateway.marvel.com/v1/public/"
PUBLIC_KEY = environ["MARVEL_PUBLIC_KEY"]
PRIVATE_KEY = environ["MARVEL_PRIVATE_KEY"]


def marvel_do_get(endpoint: str, additional_params: Dict = {}) -> Dict:
    now = datetime.now().strftime("%b %d %Y %H:%M:%S")
    hash_param = md5(f"{now}{PRIVATE_KEY}{PUBLIC_KEY}".encode("utf-8")).hexdigest()

    params = {"apikey": PUBLIC_KEY, "ts": now, "hash": hash_param}
    params.update(additional_params)

    response_string = requests.get(BASE_URL + endpoint, params=params)
    return json.loads(response_string.content.decode("utf-8"))


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

    params = {"limit": "100", "offset": str(offset)}
    response_json = marvel_do_get("characters", additional_params=params)
    return response_json["data"]["results"]


def get_character(character_id: int) -> Dict:
    print(f"Getting character {character_id}")

    response_json = marvel_do_get(f"characters/{character_id}")
    raw_character = response_json["data"]["results"][0]

    filtered_character = {
        key: raw_character[key] for key in ["id", "name", "description", "thumbnail"]
    }
    return filtered_character


if __name__ == "__main__":
    translator = Translator(to_lang="de")
    desc = get_character(1009718)["description"]
    print(translator.translate(desc))

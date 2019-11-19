import json
from datetime import datetime
from hashlib import md5
from os import environ

import requests

PUBLIC_KEY = environ["MARVEL_PUBLIC_KEY"]
PRIVATE_KEY = environ["MARVEL_PRIVATE_KEY"]

url = "http://gateway.marvel.com/v1/public/characters"
now = datetime.now().strftime("%b %d %Y %H:%M:%S")
string_to_hash = now + PRIVATE_KEY + PUBLIC_KEY
key_hash = md5(string_to_hash.encode("utf-8")).hexdigest()
# offset = 0
offset = 1200

params = {
    "apikey": PUBLIC_KEY,
    "ts": now,
    "hash": key_hash,
    "limit": "100",
    "offset": str(offset),
}
response_string = requests.get(url, params=params)
response_dict = json.loads(response_string.content.decode("utf-8"))
results = response_dict["data"]["results"]
ids = [result["id"] for result in results]

while results != []:
    print(f"Getting characters {offset} to {offset + 100}")
    offset += 100
    now = datetime.now().strftime("%b %d %Y %H:%M:%S")
    string_to_hash = now + PRIVATE_KEY + PUBLIC_KEY
    key_hash = md5(string_to_hash.encode("utf-8")).hexdigest()
    params = {
        "apikey": PUBLIC_KEY,
        "ts": now,
        "hash": key_hash,
        "limit": "100",
        "offset": str(offset),
    }
    response_string = requests.get(url, params=params)
    response_dict = json.loads(response_string.content.decode("utf-8"))
    results = response_dict["data"]["results"]
    ids += [result["id"] for result in results]


print(f"Found {len(ids)} ids")
print(ids)

import json
from datetime import datetime
from hashlib import md5
from os import environ

import requests

public_key = environ["MARVEL_PUBLIC_KEY"]
private_key = environ["MARVEL_PRIVATE_KEY"]

url = "http://gateway.marvel.com/v1/public/characters"
now = datetime.now().strftime("%b %d %Y %H:%M:%S")
string_to_hash = now + private_key + public_key
key_hash = md5(string_to_hash.encode("utf-8")).hexdigest()

params = {"apikey": public_key, "ts": now, "hash": key_hash, "limit": "100"}
response_string = requests.get(url, params=params)
response_dict = json.loads(response_string.content.decode("utf-8"))
ids = [result["id"] for result in response_dict["data"]["results"]]

print(f"Found {len(ids)} ids")
print(ids)

from typing import Dict

import requests_cache
from fastapi import FastAPI

from marvel import get_all_characters

app = FastAPI()
requests_cache.install_cache("marvel_cache", ignored_parameters=["hash", "ts"])


@app.get("/")
def read_root() -> Dict:
    return {"Hello": "World"}


@app.get("/characters")
def read_characters() -> Dict:
    return [character["id"] for character in get_all_characters()]  # type: ignore

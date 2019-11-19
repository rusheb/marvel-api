from typing import Dict

import requests_cache
from fastapi import FastAPI
from translate import Translator

import marvel

app = FastAPI()
requests_cache.install_cache("marvel_cache", ignored_parameters=["hash", "ts"])


@app.get("/")
def read_root() -> Dict:
    return {"Hello": "World"}


@app.get("/characters")
def read_characters() -> Dict:
    return [  # type: ignore
        character["id"] for character in marvel.get_all_characters()
    ]


@app.get("/characters/{character_id}")
def read_character(character_id: int, language: str = None) -> Dict:
    character = marvel.get_character(character_id)

    if language:
        translator = Translator(to_lang=language)
        character["description"] = translator.translate(character["description"])

    return character

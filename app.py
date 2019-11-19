from typing import Dict

import requests_cache
from fastapi import FastAPI
from starlette.responses import Response
from starlette.status import HTTP_400_BAD_REQUEST
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
def read_character(response: Response, character_id: int, language: str = None) -> Dict:
    character = marvel.get_character(character_id)

    if language:
        translator = Translator(to_lang=language)
        translation = translator.translate(character["description"])

        if "INVALID TARGET LANGUAGE" in translation:
            response.status_code = HTTP_400_BAD_REQUEST
            return {"Bad parameter": f"'{language}' is an invalid target language."}

        character["description"] = translation

    return character

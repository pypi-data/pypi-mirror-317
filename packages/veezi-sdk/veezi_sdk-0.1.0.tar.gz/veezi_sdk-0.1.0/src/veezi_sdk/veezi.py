from typing import List

import requests
from pydantic import BaseModel, Field
from pydantic_core import from_json

VEEZI_API_URL = "https://api.eu.veezi.com"


class Film(BaseModel):
    id: str = Field(alias="Id")
    title: str = Field(alias="Title")


def _request(endpoint: str, api_token: str) -> requests.Response:
    headers = {"VeeziAccessToken": api_token}
    return requests.get(f"{VEEZI_API_URL}/{endpoint}", headers=headers)


# v1/session + {id}
def session(api_token: str):
    pass


# v1/websession
def web_session(api_token: str):
    pass


def films(api_token: str) -> List[Film]:
    response = _request("v4/film", api_token)
    films = [Film.model_validate(film) for film in from_json(response.content)]

    return films


def films_by_id(api_token: str, id: str) -> Film:
    response = _request(f"v4/film/{id}", api_token)
    film = Film.model_validate(response.content)

    return film


# v1/filmpackage + {id}
def film_packages(api_token: str):
    pass


# v1/screen + {id}
def screen(api_token: str):
    pass


# v1/site
def site(api_token: str):
    pass


# v1/attribute + {id}
def attribute(api_token: str):
    pass

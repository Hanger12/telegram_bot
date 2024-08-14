from typing import List, Dict

import requests

from config_data.config import API_BASE_URL, RAWG_API_KEY
import json


def api_request(endpoint: str, params=None) -> requests.Response:
    if params is None:
        params = dict()
    params['key'] = RAWG_API_KEY
    return requests.get("{URL}{endpoint}".format(URL=API_BASE_URL, endpoint=endpoint),
                        params=params)


def get_game(data: dict) -> Dict:
    """Поиск по игровым эксклюзивам"""
    game = api_request(endpoint="games", params=data)
    json_games: dict = json.loads(game.text)
    return json_games


def get_stores_buy(id_game: int) -> List:
    """Поиск магазинов для конкретной игры"""
    get_stores = api_request(endpoint="games/{game_pk}/stores".format(game_pk=id_game))
    json_stores: List = json.loads(get_stores.text)['results']
    return json_stores


def get_genres() -> List:
    """Поиск по жанрам"""
    genres = api_request(endpoint="genres")
    json_genres: List = json.loads(genres.text)['results']
    return json_genres

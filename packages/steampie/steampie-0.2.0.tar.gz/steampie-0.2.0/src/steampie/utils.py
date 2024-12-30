import struct
from copy import copy
from urllib.parse import parse_qs, urlparse

import requests
from requests.structures import CaseInsensitiveDict

from .exceptions import LoginRequired, ProxyConnectionError
from .models import GameOptions

__all__ = [
    "login_required",
    "text_between",
    "texts_between",
    "account_id_to_steam_id",
    "steam_id_to_account_id",
    "merge_items_with_descriptions_from_inventory",
    "merge_items_with_descriptions_from_offers",
    "merge_items_with_descriptions_from_offer",
    "merge_items",
    "get_description_key",
    "get_key_value_from_url",
    "ping_proxy",
    "create_cookie",
]


class Credentials:
    def __init__(self, login: str, password: str, api_key: str) -> None:
        self.login = login
        self.password = password
        self.api_key = api_key


def login_required(func):
    def func_wrapper(self, *args, **kwargs):
        if not self.was_login_executed:
            raise LoginRequired("Use login method first")
        return func(self, *args, **kwargs)

    return func_wrapper


def text_between(text: str, begin: str, end: str) -> str:
    start = text.index(begin) + len(begin)
    end = text.index(end, start)

    return text[start:end]


def texts_between(text: str, begin: str, end: str):
    stop = 0

    while True:
        try:
            start = text.index(begin, stop) + len(begin)
            stop = text.index(end, start)
            yield text[start:stop]
        except ValueError:
            return


def account_id_to_steam_id(account_id: str) -> str:
    first_bytes = int(account_id).to_bytes(4, byteorder="big")
    last_bytes = 0x1100001.to_bytes(4, byteorder="big")
    return str(struct.unpack(">Q", last_bytes + first_bytes)[0])


def steam_id_to_account_id(steam_id: str) -> str:
    return str(struct.unpack(">L", int(steam_id).to_bytes(8, byteorder="big")[4:])[0])


def merge_items_with_descriptions_from_inventory(
    inventory_response: dict, game: GameOptions
) -> dict:
    inventory = inventory_response.get("assets", [])

    if not inventory:
        return {}

    descriptions = {
        get_description_key(description): description
        for description in inventory_response["descriptions"]
    }
    return merge_items(inventory, descriptions, context_id=game.context_id)


def merge_items_with_descriptions_from_offers(offers_response: dict) -> dict:
    descriptions = {
        get_description_key(offer): offer
        for offer in offers_response["response"].get("descriptions", [])
    }

    received_offers = offers_response["response"].get("trade_offers_received", [])
    sent_offers = offers_response["response"].get("trade_offers_sent", [])

    offers_response["response"]["trade_offers_received"] = [
        merge_items_with_descriptions_from_offer(offer, descriptions)
        for offer in received_offers
    ]

    offers_response["response"]["trade_offers_sent"] = [
        merge_items_with_descriptions_from_offer(offer, descriptions)
        for offer in sent_offers
    ]

    return offers_response


def merge_items_with_descriptions_from_offer(offer: dict, descriptions: dict) -> dict:
    merged_items_to_give = merge_items(offer.get("items_to_give", []), descriptions)
    merged_items_to_receive = merge_items(
        offer.get("items_to_receive", []), descriptions
    )

    offer["items_to_give"] = merged_items_to_give
    offer["items_to_receive"] = merged_items_to_receive

    return offer


def merge_items(items: list[dict], descriptions: dict, **kwargs) -> dict:
    merged_items = {}

    for item in items:
        description_key = get_description_key(item)
        description = copy(descriptions[description_key])
        item_id = item.get("id") or item["assetid"]
        description["contextid"] = item.get("contextid") or kwargs["context_id"]
        description["id"] = item_id
        description["amount"] = item["amount"]
        merged_items[item_id] = description

    return merged_items


def get_description_key(item: dict) -> str:
    return f'{item["classid"]}_{item["instanceid"]}'


def get_key_value_from_url(url: str, key: str, case_sensitive: bool = True) -> str:
    params = urlparse(url).query
    return (
        parse_qs(params)[key][0]
        if case_sensitive
        else CaseInsensitiveDict(parse_qs(params))[key][0]
    )


def ping_proxy(proxies: dict) -> bool:
    try:
        requests.get("https://steamcommunity.com/", proxies=proxies)
        return True
    except Exception:
        raise ProxyConnectionError("Proxy not working for steamcommunity.com")


def create_cookie(name: str, cookie: str, domain: str) -> dict:
    return {"name": name, "value": cookie, "domain": domain}

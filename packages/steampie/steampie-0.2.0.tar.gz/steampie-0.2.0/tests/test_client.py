import pytest

from steampie.client import SteamClient
from steampie.exceptions import LoginRequired
from steampie.models import Asset, GameOptions


def test_steam_login(client: SteamClient) -> None:
    assert client.is_session_alive()


def test_get_steam_id(client: SteamClient, steam_guard_file) -> None:
    assert client.steam_id == str(steam_guard_file["Session"]["SteamID"])


def test_sessionid_cookie(client: SteamClient) -> None:
    community_cookies = client._session.cookies.get_dict("steamcommunity.com")
    store_cookies = client._session.cookies.get_dict("store.steampowered.com")

    assert "sessionid" in community_cookies
    assert "sessionid" in store_cookies


def test_get_my_inventory(client: SteamClient) -> None:
    inventory = client.get_my_inventory(GameOptions.CS)
    assert inventory is not None


def test_get_partner_inventory(client: SteamClient) -> None:
    partner_id = "76561198449257208"
    game = GameOptions.TF2
    inventory = client.get_partner_inventory(partner_id, game)
    assert inventory is not None


def test_get_trade_offers_summary(client: SteamClient) -> None:
    summary = client.get_trade_offers_summary()
    assert summary is not None


def test_get_trade_offers(client: SteamClient) -> None:
    offers = client.get_trade_offers()
    assert offers is not None


# def test_get_trade_offer() -> None:
#     trade_offer_id = "488991480"
#     offer = client.get_trade_offer(trade_offer_id)
#     assert offer is not None


# def test_accept_trade_offer() -> None:
#     trade_offer_id = "1451378159"
#     response_dict = client.accept_trade_offer(trade_offer_id)
#     assert response_dict is not None


# def test_decline_trade_offer() -> None:
#     trade_offer_id = "1449530707"
#     response_dict = client.decline_trade_offer(trade_offer_id)
#     assert response_dict["response"] == {}


# def test_cancel_trade_offer() -> None:
#     trade_offer_id = "1450637835"
#     response_dict = client.cancel_trade_offer(trade_offer_id)
#     assert response_dict["response"] == {}


def test_make_offer_url(
    client: SteamClient, partner_steam_id: str, partner_trade_url: str
) -> None:
    game = GameOptions.TF2
    my_items = client.get_my_inventory(GameOptions.TF2)
    partner_items = client.get_partner_inventory(partner_steam_id, game)
    my_first_item = next(iter(my_items.values()))
    partner_first_item = next(iter(partner_items.values()))
    my_asset = Asset(my_first_item["id"], game)
    partner_asset = Asset(partner_first_item["id"], game)
    response = client.make_offer_with_url(
        [my_asset], [partner_asset], partner_trade_url, "test offer"
    )

    assert response is not None
    assert "tradeofferid" in response


def test_make_offer(client: SteamClient, partner_steam_id: str) -> None:
    game = GameOptions.TF2
    my_items = client.get_my_inventory(GameOptions.TF2)
    partner_items = client.get_partner_inventory(partner_steam_id, game)
    my_first_item = next(iter(my_items.values()))
    partner_first_item = next(iter(partner_items.values()))
    my_asset = Asset(my_first_item["id"], game)
    partner_asset = Asset(partner_first_item["id"], game)
    response = client.make_offer(
        [my_asset], [partner_asset], partner_steam_id, "test offer"
    )

    assert response is not None
    assert "tradeofferid" in response


def test_get_escrow_duration(client: SteamClient, partner_trade_url: str) -> None:
    response = client.get_escrow_duration(partner_trade_url)
    assert response == 0


def test_logout(client: SteamClient) -> None:
    assert client.is_session_alive()
    client.logout()
    assert not client.was_login_executed


def test_accept_trade_offer_without_login(credentials: dict) -> None:
    client = SteamClient(credentials["api_key"], None, None, None, None)

    with pytest.raises(LoginRequired):
        client.accept_trade_offer("id")

def test_get_items_returns_seeded_catalog(client) -> None:
    response = client.get("/items")

    assert response.status_code == 200
    payload = response.json()
    assert [item["id"] for item in payload["items"]] == [
        "itm_conflict-lab",
        "itm_storage-decision",
        "itm_agent-roster",
        "itm_release-brief",
        "itm_contract-pass",
    ]


def test_get_item_returns_detail(client) -> None:
    response = client.get("/items/itm_storage-decision")

    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == "itm_storage-decision"
    assert "open_questions" in payload
    assert "active_agent_ids" in payload


def test_missing_item_returns_not_found(client) -> None:
    response = client.get("/items/does-not-exist")

    assert response.status_code == 404
    payload = response.json()
    assert payload["error"] == "resource_not_found"
    assert payload["context"]["resource_type"] == "item"

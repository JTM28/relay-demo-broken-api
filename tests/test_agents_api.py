def test_get_agents_returns_seeded_roster(client) -> None:
    response = client.get("/agents")

    assert response.status_code == 200
    payload = response.json()
    assert [agent["id"] for agent in payload["agents"]] == [
        "agt_harbor",
        "agt_nova",
        "agt_orchid",
        "agt_rune",
    ]


def test_get_agent_returns_detail(client) -> None:
    response = client.get("/agents/agt_nova")

    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == "agt_nova"
    assert payload["specialty"] == "backend"
    assert "strengths" in payload

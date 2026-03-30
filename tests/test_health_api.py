def test_health_reports_seed_metadata(client) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["service"] == "Relay Coordination API"
    assert payload["environment"] == "local"
    assert payload["storage_mode"] == "in_memory"
    assert payload["resource_counts"] == {"items": 5, "agents": 4, "sessions": 2}

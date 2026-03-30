def test_openapi_includes_full_route_surface(client) -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200
    schema = response.json()
    paths = schema["paths"]

    assert "/health" in paths
    assert "/items" in paths
    assert "/items/{item_id}" in paths
    assert "/agents" in paths
    assert "/agents/{agent_id}" in paths
    assert "/sessions" in paths
    assert "/sessions/{session_id}" in paths
    assert "/sessions/{session_id}/compare" in paths

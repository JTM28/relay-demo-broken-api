def test_get_sessions_returns_seeded_sessions(client) -> None:
    response = client.get("/sessions")

    assert response.status_code == 200
    payload = response.json()
    assert [session["id"] for session in payload["sessions"]] == [
        "ses_conflict-lab",
        "ses_storage-path",
    ]


def test_get_session_returns_detail(client) -> None:
    response = client.get("/sessions/ses_storage-path")

    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == "ses_storage-path"
    assert len(payload["checkpoints"]) == 3
    assert len(payload["positions"]) == 2


def test_compare_session_options_returns_neutral_recommendation(client) -> None:
    response = client.post(
        "/sessions/ses_storage-path/compare",
        json={
            "focus_areas": ["delivery_speed", "operability", "adaptability"],
            "left": {
                "label": "Path Alpha",
                "summary": "Lean into the smallest workable surface.",
                "strengths": ["simple rollout", "lower coordination cost", "faster feedback"],
                "risks": [],
                "assumptions": ["team can revisit the shape later"],
                "change_surface": "contained",
                "operability": "high",
                "adaptability": "high",
            },
            "right": {
                "label": "Path Beta",
                "summary": "Expand the surface more aggressively up front.",
                "strengths": ["more detail"],
                "risks": ["more moving parts", "slower review"],
                "assumptions": [],
                "change_surface": "broad",
                "operability": "low",
                "adaptability": "low",
            },
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["session_id"] == "ses_storage-path"
    assert payload["leading_option"] == "Path Alpha"
    assert payload["confidence"] in {"low", "medium", "high"}
    assert payload["left"]["label"] == "Path Alpha"
    assert payload["right"]["label"] == "Path Beta"

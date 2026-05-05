def test_create_team(client):
    resp = client.post(
        "/api/teams/", json={"name": "Support A", "description": "Main support"}
    )
    assert resp.status_code == 201
    assert resp.json()["name"] == "Support A"


def test_list_teams(client):
    client.post("/api/teams/", json={"name": "Team A"})
    client.post("/api/teams/", json={"name": "Team B"})
    resp = client.get("/api/teams/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_soft_delete_team(client):
    create_resp = client.post("/api/teams/", json={"name": "Team A"})
    team_id = create_resp.json()["id"]
    del_resp = client.delete(f"/api/teams/{team_id}")
    assert del_resp.status_code == 204
    list_resp = client.get("/api/teams/")
    assert len(list_resp.json()) == 0

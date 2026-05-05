def test_create_client(client):
    resp = client.post(
        "/api/clients/", json={"name": "Acme Corp", "email": "contact@acme.com"}
    )
    assert resp.status_code == 201
    assert resp.json()["name"] == "Acme Corp"


def test_create_client_invalid_email(client):
    resp = client.post(
        "/api/clients/", json={"name": "Acme Corp", "email": "bad-email"}
    )
    assert resp.status_code == 422


def test_list_clients_with_pagination(client):
    for i in range(5):
        client.post(
            "/api/clients/", json={"name": f"Client {i}", "email": f"c{i}@example.com"}
        )
    resp = client.get("/api/clients/?skip=0&limit=3")
    assert resp.status_code == 200
    assert len(resp.json()) == 3

    resp2 = client.get("/api/clients/?skip=3&limit=3")
    assert resp2.status_code == 200
    assert len(resp2.json()) == 2


def test_soft_delete_client(client):
    create_resp = client.post(
        "/api/clients/", json={"name": "Acme", "email": "a@acme.com"}
    )
    client_id = create_resp.json()["id"]
    del_resp = client.delete(f"/api/clients/{client_id}")
    assert del_resp.status_code == 204
    list_resp = client.get("/api/clients/")
    assert len(list_resp.json()) == 0

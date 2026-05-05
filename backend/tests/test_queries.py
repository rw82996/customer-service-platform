def _create_client(client):
    resp = client.post(
        "/api/clients/", json={"name": "Acme", "email": "contact@acme.com"}
    )
    return resp.json()["id"]


def test_create_query(client):
    client_id = _create_client(client)
    resp = client.post(
        "/api/queries/",
        json={
            "subject": "Test query",
            "description": "Description here",
            "priority": "high",
            "client_id": client_id,
        },
    )
    assert resp.status_code == 201
    assert resp.json()["subject"] == "Test query"
    assert resp.json()["priority"] == "high"
    assert resp.json()["status"] == "open"


def test_create_query_invalid_priority(client):
    client_id = _create_client(client)
    resp = client.post(
        "/api/queries/",
        json={
            "subject": "Test",
            "description": "Desc",
            "priority": "super_urgent",
            "client_id": client_id,
        },
    )
    assert resp.status_code == 422


def test_update_query_status(client):
    client_id = _create_client(client)
    create_resp = client.post(
        "/api/queries/",
        json={
            "subject": "Test",
            "description": "Desc",
            "client_id": client_id,
        },
    )
    query_id = create_resp.json()["id"]
    update_resp = client.patch(f"/api/queries/{query_id}", json={"status": "resolved"})
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "resolved"
    assert update_resp.json()["resolved_at"] is not None


def test_update_query_invalid_status(client):
    client_id = _create_client(client)
    create_resp = client.post(
        "/api/queries/",
        json={
            "subject": "Test",
            "description": "Desc",
            "client_id": client_id,
        },
    )
    query_id = create_resp.json()["id"]
    update_resp = client.patch(
        f"/api/queries/{query_id}", json={"status": "invalid_status"}
    )
    assert update_resp.status_code == 422


def test_soft_delete_query(client):
    client_id = _create_client(client)
    create_resp = client.post(
        "/api/queries/",
        json={
            "subject": "Test",
            "description": "Desc",
            "client_id": client_id,
        },
    )
    query_id = create_resp.json()["id"]
    del_resp = client.delete(f"/api/queries/{query_id}")
    assert del_resp.status_code == 204
    list_resp = client.get("/api/queries/")
    assert len(list_resp.json()) == 0


def test_add_response_to_query(client):
    client_id = _create_client(client)
    staff_resp = client.post(
        "/api/staff/", json={"name": "Alice", "email": "alice@example.com"}
    )
    staff_id = staff_resp.json()["id"]
    query_resp = client.post(
        "/api/queries/",
        json={
            "subject": "Test",
            "description": "Desc",
            "client_id": client_id,
        },
    )
    query_id = query_resp.json()["id"]
    resp = client.post(
        f"/api/queries/{query_id}/responses",
        json={
            "message": "Looking into this",
            "staff_id": staff_id,
            "is_internal_note": False,
        },
    )
    assert resp.status_code == 201
    assert resp.json()["message"] == "Looking into this"
    assert resp.json()["is_internal_note"] is False


def test_list_queries_with_pagination(client):
    client_id = _create_client(client)
    for i in range(5):
        client.post(
            "/api/queries/",
            json={
                "subject": f"Query {i}",
                "description": "Desc",
                "client_id": client_id,
            },
        )
    resp = client.get("/api/queries/?skip=0&limit=3")
    assert resp.status_code == 200
    assert len(resp.json()) == 3

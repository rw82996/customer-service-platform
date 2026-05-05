def test_create_staff(client):
    resp = client.post(
        "/api/staff/",
        json={"name": "Alice", "email": "alice@example.com", "role": "agent"},
    )
    assert resp.status_code == 201
    assert resp.json()["name"] == "Alice"
    assert resp.json()["role"] == "agent"


def test_create_staff_with_invalid_role(client):
    resp = client.post(
        "/api/staff/",
        json={"name": "Bob", "email": "bob@example.com", "role": "invalid_role"},
    )
    assert resp.status_code == 422


def test_create_staff_with_invalid_email(client):
    resp = client.post(
        "/api/staff/", json={"name": "Bob", "email": "not-an-email", "role": "agent"}
    )
    assert resp.status_code == 422


def test_list_staff(client):
    client.post(
        "/api/staff/",
        json={"name": "Alice", "email": "alice@example.com", "role": "agent"},
    )
    client.post(
        "/api/staff/",
        json={"name": "Bob", "email": "bob@example.com", "role": "supervisor"},
    )
    resp = client.get("/api/staff/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_soft_delete_staff(client):
    create_resp = client.post(
        "/api/staff/", json={"name": "Alice", "email": "alice@example.com"}
    )
    staff_id = create_resp.json()["id"]
    del_resp = client.delete(f"/api/staff/{staff_id}")
    assert del_resp.status_code == 204
    list_resp = client.get("/api/staff/")
    assert len(list_resp.json()) == 0

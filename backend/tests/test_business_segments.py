def test_create_segment(client):
    resp = client.post(
        "/api/business-segments/",
        json={"name": "Lending", "description": "Lending products"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Lending"
    assert data["description"] == "Lending products"
    assert data["is_active"] is True


def test_list_segments(client):
    client.post("/api/business-segments/", json={"name": "Lending"})
    client.post("/api/business-segments/", json={"name": "Payments"})
    resp = client.get("/api/business-segments/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_get_segment(client):
    create_resp = client.post("/api/business-segments/", json={"name": "Lending"})
    seg_id = create_resp.json()["id"]
    resp = client.get(f"/api/business-segments/{seg_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Lending"


def test_update_segment(client):
    create_resp = client.post("/api/business-segments/", json={"name": "Lending"})
    seg_id = create_resp.json()["id"]
    resp = client.patch(
        f"/api/business-segments/{seg_id}", json={"description": "Updated"}
    )
    assert resp.status_code == 200
    assert resp.json()["description"] == "Updated"


def test_soft_delete_segment(client):
    create_resp = client.post("/api/business-segments/", json={"name": "Lending"})
    seg_id = create_resp.json()["id"]
    del_resp = client.delete(f"/api/business-segments/{seg_id}")
    assert del_resp.status_code == 204
    # Should not appear in list
    list_resp = client.get("/api/business-segments/")
    assert len(list_resp.json()) == 0
    # Should return 404 on direct access
    get_resp = client.get(f"/api/business-segments/{seg_id}")
    assert get_resp.status_code == 404

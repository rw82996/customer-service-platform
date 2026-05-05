def test_register_and_login(client):
    # Register
    reg_resp = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Alice",
            "email": "alice@example.com",
            "password": "securepassword123",
            "role": "admin",
        },
    )
    assert reg_resp.status_code == 201
    assert reg_resp.json()["email"] == "alice@example.com"

    # Login
    login_resp = client.post(
        "/api/v1/auth/token",
        data={
            "username": "alice@example.com",
            "password": "securepassword123",
        },
    )
    assert login_resp.status_code == 200
    assert "access_token" in login_resp.json()
    assert login_resp.json()["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "name": "Bob",
            "email": "bob@example.com",
            "password": "password123",
        },
    )
    login_resp = client.post(
        "/api/v1/auth/token",
        data={
            "username": "bob@example.com",
            "password": "wrongpassword",
        },
    )
    assert login_resp.status_code == 401


def test_register_duplicate_email(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "name": "Alice",
            "email": "alice@example.com",
            "password": "password123",
        },
    )
    dup_resp = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Alice 2",
            "email": "alice@example.com",
            "password": "password456",
        },
    )
    assert dup_resp.status_code == 400

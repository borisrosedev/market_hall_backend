import pytest

@pytest.mark.integration
def test_create_user(client):
    payload = {"email": "bob@gmail.com", "password": "caroline123", "firstname":"bob", "lastname":"dupont"}
    res = client.post("/api/v1/users/", json=payload)
    assert res.status_code in (200, 201), f"{res.status_code} body={res.data!r}"

    data = res.get_json(silent=True)
    assert data is not None, f"none-json: CT={res.headers.get('Content-Type')} body={res.data!r}"
    assert data.get("message") == "user created with a cart"
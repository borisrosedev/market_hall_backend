import pytest


@pytest.mark.integration
def test_get_updated_password_current_user(client, make_user_id):

    id, email, password = make_user_id()

    res_login = client.post("/api/v1/auth/login", json={"email": email, "password":password })
    assert res_login.status_code == 200 

    payload = {"email": email, "password": "largo123"}
    res = client.put(f"/api/v1/users/{id}", json=payload)
    assert res.status_code is 200, f"{res.status_code} body={res.data!r}"

    res_login = client.post("/api/v1/auth/login", json={"email": email, "password":"largo123" })
    assert res_login.status_code == 200 
 


@pytest.mark.integration
def test_create_user(client):
    payload = {"email": "bob@gmail.com", "password": "caroline123", "firstname":"bob", "lastname":"dupont"}
    res = client.post("/api/v1/users/", json=payload)
    assert res.status_code in (200, 201), f"{res.status_code} body={res.data!r}"

    data = res.get_json(silent=True)
    assert data is not None, f"none-json: CT={res.headers.get('Content-Type')} body={res.data!r}"
    assert data.get("message") == "user created with a cart"
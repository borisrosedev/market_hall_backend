from http.cookies import SimpleCookie
import pytest
import logging 

logging.basicConfig(level=logging.INFO)

COOKIE_NAME = "session"

@pytest.mark.integration
def test_get_current_admin(client, make_admin_id):
    id, email, password = make_admin_id()
    res_login = client.post("api/v1/auth/login", json={"email": email, "password" : password })
    assert res_login.status_code is 200, f"{res_login.status_code} body={res_login.data!r}"

    res_get_me = client.get("api/v1/users/me")
    parsed_res = res_get_me.get_json(silent=True)
    assert res_get_me.status_code is 200
    assert  parsed_res.get("user").get("role") == "admin"

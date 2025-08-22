# tests/integration/auth/test_login_cookie.py
from http.cookies import SimpleCookie
import pytest

COOKIE_NAME = "session"


# helper
def _get_cookie(response, name: str):
    cookies = SimpleCookie()
    for header in response.headers.getlist("Set-Cookie"):
        cookies.load(header)
    return cookies.get(name) 

@pytest.mark.integration
def test_login_sets_cookie(client, make_user):
    email, pwd = make_user()

    res = client.post("/api/v1/auth/login", json={"email": email, "password": pwd})
    assert res.status_code == 200

    # Is Set-Cookie Header present ?
    assert "Set-Cookie" in res.headers

    # Clean Parsing
    cookies = SimpleCookie()
    for header in res.headers.getlist("Set-Cookie"):
        cookies.load(header)

    assert COOKIE_NAME in cookies, res.headers.getlist("Set-Cookie")

    cookie = cookies[COOKIE_NAME]
    assert bool(cookie['httponly']) == True or cookie['httponly'] == "True"
    #assert c["secure"] == False
    #assert c["samesite"].lower() in ("lax", "strict", "none")



@pytest.mark.integration
def test_authenticated_route_uses_cookie_implicitly(client, make_user):
    email, pwd = make_user()

    r_login = client.post("/api/v1/auth/login", json={"email": email, "password": pwd})
    assert r_login.status_code == 200

    # Call of a protected route - Cookie is sent automatically
    r_me = client.get("/api/v1/users/me")
    assert r_me.status_code == 200
    data = r_me.get_json(silent=True)
    assert data and data.get("user", {}).get("email") == email  # adapte à ta réponse


@pytest.mark.integration
def test_login_wrong_password_does_not_set_cookie(client, make_user):
    email, _ = make_user()

    res = client.post("/api/v1/auth/login", json={"email": email, "password": "nicolas"})
    assert res.status_code == 400
    all_set_cookie = res.headers.getlist("Set-Cookie")
    assert not any(COOKIE_NAME in sc for sc in all_set_cookie)


@pytest.mark.integration
def test_cookie_flags(client, make_user):
    email, pwd = make_user()
    r_login = client.post("/api/v1/auth/login", json={"email": email, "password": pwd})

    cookie = _get_cookie(response=r_login, name=COOKIE_NAME)
    assert cookie is not None
    assert cookie.get("httponly") in (True, "true")
    # assert cookie.secure is True
    #assert (cookie.get("samesite") or "").lower() in ("lax", "strict", "none")


@pytest.mark.integration
def test_cors_allows_credentials_on_login(client, make_user):
    email, pwd = make_user()
    r = client.post("/api/v1/auth/login", json={"email": email, "password": pwd}, headers={"Origin": "http://localhost:3000"})
    assert r.headers.get("Access-Control-Allow-Credentials") == "true"
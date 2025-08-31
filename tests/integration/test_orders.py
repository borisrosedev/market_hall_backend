import pytest

@pytest.mark.integration
def test_create_orders(client, make_user,make_order):
    email, pwd = make_user() 
    res = client.post("/api/v1/auth/login", json={"email": email, "password": pwd})
    assert res.status_code == 200

    # Call of a protected route - Cookie is sent automatically
    r_me = client.get("/api/v1/users/me")
    assert r_me.status_code == 200
    data = r_me.get_json(silent=True)
    assert data and data.get("user", {}).get("email") == email  # adapte à ta réponse
    
    user_id = data.get("user")['id']  
    # order 
    #user_id, amounts_cents, currency, status = make_order    
    #r_order = client.post("/api/v1/orders", json={"user_id": user_id, "amounts_cents":amounts_cents, "currency":currency,"status":status})
    #assert r_order.status_code == 200
    
    payload = { "user_id":user_id,"amounts_cents":10000099,"currency":"USD","status":"created"}
    r_order = client.post("/api/v1/orders/", json=payload)
    assert r_order.status_code in (200, 201), f"{r_order.status_code} body={r_order.data!r}"
    
    data = r_order.get_json(silent=True)
    assert data is not None, f"none-json: CT={r_order.headers.get('Content-Type')} body={r_order.data!r}"
    assert data.get("message") == "order created" 
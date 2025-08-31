import pytest

@pytest.mark.integration
def test_create_order(client,user_with_order):
    data =user_with_order() 
    data_user = data['user'] 
    data_order = data['order']
    assert data_user ['id'] is not None
    assert data_order['id'] is not None 
     
    #user_id , email,password = data_user 
    user_id= data['user'] ["id"]
    email = data['user'] ["email"]
    password = data['user'] ["password"]
    
    #id, amounts_cents, currency, status = data_order
    order_id= data['order'] ["id"]
    amounts_cents= data['order'] ["amounts_cents"]
    currency = data['order'] ["currency"]
    status = data['order'] ["status"] 
     
    # Login  
    r_login = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert r_login.status_code == 200 
    
    # me 
    r_me = client.get("/api/v1/users/me")
    assert r_me.status_code == 200
    data = r_me.get_json(silent=True)
    assert data and data.get("user", {}).get("email") == email  
    
    # order created 
    payload = { "user_id":user_id,"amounts_cents":amounts_cents,"currency":currency,"status":status}
    r_order = client.post("/api/v1/orders/", json=payload)
    assert r_order.status_code in (200, 201), f"{r_order.status_code} body={r_order.data!r}"
     
    data = r_order.get_json(silent=True)
    assert data is not None, f"none-json: CT={r_order.headers.get('Content-Type')} body={r_order.data!r}"
    assert data.get("message") == "order created" 
  
    
    
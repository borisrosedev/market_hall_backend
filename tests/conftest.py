import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
import pytest
from pathlib import Path
from typing import Union
from faker import Faker
from app import create_app
from app.database import db as _db
from app.database.models import User,Cart, Order

@pytest.fixture(scope="session")
def faker():
    return Faker()

@pytest.fixture(scope="session")
def app(tmp_path_factory):
    # temporary uploads folder for tests session
    uploads_dir = tmp_path_factory.mktemp("uploads")
   
    app = create_app(config_override={
        "TESTING": True,
        # DB sqlite file epheral and isolated
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{tmp_path_factory.mktemp('db') / 'test.db'}",
        "UPLOAD_FOLDER": uploads_dir,
        "SECRET_KEY": "test-secret",
    })
    print (tmp_path_factory)
    return app

@pytest.fixture()
def client(app):
    return app.test_client()
 
@pytest.fixture(autouse=True)
def _clean_db(app):
    """
    Clean the db after each test
    """
    with app.app_context():
        _db.drop_all()
        _db.create_all()
        yield
        _db.session.remove()

# To access session while testing:
@pytest.fixture()
def db(app):
    with app.app_context():
        yield _db

@pytest.fixture()
def make_user(app):
    """Create a user in db and return email and (plain) password """
    def _make_user(email="loic@example.com", password="caroline123", firstname="loic", lastname="dupont"):
        with app.app_context():
            u = User(
                email=email,
                firstname=firstname,
                lastname=lastname
            )
            u.password = password
            _db.session.add(u)
            _db.session.flush() 
            cart = Cart(user_id=u.id)
            _db.session.add(cart)
            _db.session.commit()
        return email, password,
    return _make_user


@pytest.fixture()
def make_admin_id(app):
    def _make_admin_id(email="admin_boris@gmail.com", password="caroline123", firstname="boris", lastname="shang"):
        with app.app_context():
            u = User(
                email=email,
                firstname=firstname,
                lastname=lastname,
                role="admin"
            )
            u.password = password
            _db.session.add(u)
            _db.session.flush() 
            cart = Cart(user_id=u.id)
            _db.session.add(cart)
            _db.session.commit()
            id = u.id
        return id, email, password
    return _make_admin_id

@pytest.fixture()
def make_user_id(app):
    """Create a user in db and return id, email and (plain) password """
    def _make_user_id(email="loic@example.com", password="caroline123", firstname="loic", lastname="dupont"):
        with app.app_context():
            u = User(
                email=email,
                firstname=firstname,
                lastname=lastname
            )
            u.password = password
            _db.session.add(u)
            _db.session.flush() 
            cart = Cart(user_id=u.id)
            _db.session.add(cart)
            _db.session.commit()
            id = u.id
        return id, email, password
    return _make_user_id

@pytest.fixture()
def user_with_order(app, make_user_id):
    """Create a user and an order for that user"""
    def _create_user_with_order(
        email="loic@example.com", 
        password="caroline123", 
        firstname="bob", 
        lastname="dupont",
        amounts_cents=10000098, 
        currency="CHF", 
        status="created"
    ):
        # Created user and get id 
        user_id, email, password = make_user_id(email, password, firstname, lastname)
          
        # Created Order with user_id
        with app.app_context():
            o = Order(
                user_id=user_id,
                amounts_cents=amounts_cents,
                currency=currency,
                status=status
            )
            _db.session.add(o)
            _db.session.commit()
            id = o.id
               
        return {
            'user': {'id': user_id,'email': email, 'password': password},
            'order': {'id': id, 'amounts_cents': amounts_cents, 'currency': currency, 'status': status}
        }
    return _create_user_with_order

"""
@pytest.fixture()
def make_order(app,client,make_user):
    
    #email, pwd = make_user() 
    #res = client.post("/api/v1/auth/login", json={"email": email, "password": pwd})
    r_me = client.get("/api/v1/users/me")
    data = r_me.get_json(silent=True)
    print(r_me)
    def _make_order(user_id=1 , amounts_cents="10000098", currency="CHN", status="created"):
        with app.app_context():
            o = Order(
                user_id=user_id,
                amounts_cents=amounts_cents,
                currency=currency,
                status=status
            )
            o.user_id = user_id
            o.amounts_cents=amounts_cents
            o.currency=currency
            o.status=status
            _db.session.add(o)
            _db.session.flush() 
            _db.session.commit()
        return  user_id, amounts_cents, currency, status
    return _make_order
"""
@pytest.fixture()
def load_json():
    def _load(path: Union[str, os.PathLike]):
        return json.loads(Path(path).read_text(encoding="utf-8"))
    return _load

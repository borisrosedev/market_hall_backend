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
    print ("uploads_dir")
    print (uploads_dir)
    app = create_app(config_override={
        "TESTING": True,
        # DB sqlite file epheral and isolated
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{tmp_path_factory.mktemp('db') / 'test.db'}",
        "UPLOAD_FOLDER": uploads_dir,
        "SECRET_KEY": "test-secret",
    })
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
        return email, password
    return _make_user

@pytest.fixture()
def make_order(app):
    """Create a order in db and return id, amounts_cents, currency, status """
    def _make_order(user_id=1, amounts_cents="10000098", currency="CHN", status="created"):
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

@pytest.fixture()
def load_json():
    def _load(path: Union[str, os.PathLike]):
        return json.loads(Path(path).read_text(encoding="utf-8"))
    return _load

from __future__ import annotations
import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from .api.routes import __all_routes__ as routes
from .database import db
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cur = dbapi_connection.cursor()
        cur.execute("PRAGMA foreign_keys=ON;")
        cur.close()

def create_app(config_override: dict | None = None):
    """CREATE THE APP"""
    load_dotenv()

    app = Flask(__name__)

    # Default Config
    app.config.update({
        "TESTING": False,
        "SQLALCHEMY_DATABASE_URI": os.getenv("SQLALCHEMY_DATABASE_URI"),
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "MAX_CONTENT_LENGTH": 16 * 1000 * 1000,
        "UPLOAD_FOLDER": Path(os.getcwd()) / "uploads",
        "PERMANENT_SESSION_LIFETIME": timedelta(minutes=15),
        "SECRET_KEY": os.getenv("SECRET_KEY", "boris-secret"),
    })

    # Allow tests to clean overide
    if config_override:
        app.config.update(config_override)

    # CORS
    CORS(app, supports_credentials=True)

    # Blueprints
    app.register_blueprint(routes.api_v1_users)
    app.register_blueprint(routes.api_v1_admin)
    app.register_blueprint(routes.api_v1_auth)
    app.register_blueprint(routes.api_v1_products)
    app.register_blueprint(routes.api_v1_carts)
    app.register_blueprint(routes.api_v1_notifications)
    app.register_blueprint(routes.api_v1_orders)
    app.register_blueprint(routes.api_v1_order_addresses)
    app.register_blueprint(routes.api_v1_order_items)
    app.register_blueprint(routes.static_files)

    # DB
    db.init_app(app)
    with app.app_context():
        from .models.db_models import __all_db_models__ 
        db.create_all()


    # Uploads Folder (usable prod and test)
    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)

    return app

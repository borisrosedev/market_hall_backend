import os 
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from .routes import api_v1_users

from .database import db

def create_app():
    """ CREATE THE APP """
    app = Flask(__name__)
    load_dotenv()
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    CORS(app, supports_credentials=True)
    app.register_blueprint(api_v1_users)
    db.init_app(app)
    with app.app_context():
        from .database.models import User
        db.create_all()


    return app

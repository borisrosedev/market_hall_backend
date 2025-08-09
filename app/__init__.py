import os 
from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from .routes import api_v1_users, api_v1_auth

from .database import db

def create_app():
    """ CREATE THE APP """
    load_dotenv()
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.secret_key=os.getenv("SECRET_KEY")
    app.config['PERMANENT_SESSION_LIFETIME']= timedelta(minutes=15)
    CORS(app, supports_credentials=True)
    app.register_blueprint(api_v1_users)
    app.register_blueprint(api_v1_auth)
    db.init_app(app)
    with app.app_context():
        from .database.models import User
        db.create_all()


    return app

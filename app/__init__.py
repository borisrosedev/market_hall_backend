import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from .routes import api_v1_users, api_v1_auth, api_v1_carts, api_v1_products, static_files, api_v1_notifications, api_v1_admin
from .database import db


def create_app():
    """ CREATE THE APP """
    load_dotenv()
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = Path(os.getcwd()+"/uploads")
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.secret_key=os.getenv("SECRET_KEY")
    app.config['PERMANENT_SESSION_LIFETIME']= timedelta(minutes=15)
    CORS(app, supports_credentials=True)
    app.register_blueprint(api_v1_users)
    app.register_blueprint(api_v1_admin)
    app.register_blueprint(api_v1_auth)
    app.register_blueprint(api_v1_products)
    app.register_blueprint(api_v1_carts)
    app.register_blueprint(api_v1_notifications)
    app.register_blueprint(static_files)
    db.init_app(app)
    with app.app_context():
        from .database.models import User,Cart,CartProduct,Product,Notification
        db.create_all()


    return app

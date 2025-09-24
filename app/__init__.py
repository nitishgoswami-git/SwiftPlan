from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import pymysql
pymysql.install_as_MySQLdb()

db = SQLAlchemy()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    print("DB URI:", os.getenv("DATABASE_URI"))
    print("SECRET_KEY:", os.getenv("SECRET_KEY"))

    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "default_secret")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False         # fixed type

    db.init_app(app)  # proper initialization

    # Import and register blueprints
    from app.routes.auth import auth_bp
    from app.routes.task import task_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)

    return app

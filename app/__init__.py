from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy # type: ignore
import os
from os import getenv
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt  # type: ignore # Menambahkan import bcrypt
from flask_socketio import SocketIO, emit  # Menambahkan import SocketIO dan emit


load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()  # Inisialisasi Bcrypt dengan aplikasi Flask
socketio = SocketIO()  # Inisialisasi SocketIO

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    socketio.init_app(app)  # Inisialisasi SocketIO dengan aplikasi Flask

    with app.app_context():
        from .routes import main
        from app.models.user import User
        from app.models.chatroom import ChatRoom
        from app.models.chat import Chat
        


        app.register_blueprint(main)

    return app
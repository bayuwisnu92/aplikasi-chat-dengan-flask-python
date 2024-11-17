from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy # type: ignore
import os
from os import getenv
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt  # type: ignore
from flask_socketio import SocketIO, emit  # Menambahkan import SocketIO dan emit
from werkzeug.utils import secure_filename



load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()  # Inisialisasi Bcrypt dengan aplikasi Flask
socketio = SocketIO()  # Inisialisasi SocketIO dengan aplikasi Flask

# Definisikan ALLOWED_EXTENSIONS secara lokal
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Fungsi untuk mengizinkan tipe file tertentu
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Membuat folder uploads jika belum ada
    

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    socketio.init_app(app)  # Inisialisasi SocketIO dengan aplikasi Flask

    # Registrasi blueprint
    from .routes import main  # Mengimpor blueprint
    app.register_blueprint(main)
    from .friend_routes import friend_bp
    app.register_blueprint(friend_bp)
    from .group_routes import group_bp
    app.register_blueprint(group_bp)
    



    return app


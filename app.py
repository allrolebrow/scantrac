from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import date
import os

# Load environment variables
load_dotenv()

# ================= INIT EXTENSIONS =================
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)

    # ================= CONFIG =================
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret')

    # 🔥 DATABASE CONFIG (SUPPORT LOCAL & PRODUCTION)
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        # Fix untuk Railway (mysql:// -> mysql+pymysql://)
        if database_url.startswith("mysql://"):
            database_url = database_url.replace("mysql://", "mysql+pymysql://", 1)

        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
            f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', 3306)}/{os.getenv('DB_NAME')}"
        )

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['BASE_URL'] = os.getenv('BASE_URL', 'http://localhost:5000')
    app.config['QR_FOLDER'] = os.path.join(app.root_path, 'static', 'qrcodes')

    # 🔥 AUTO CREATE QR FOLDER (BIAR GAK ERROR)
    os.makedirs(app.config['QR_FOLDER'], exist_ok=True)

    # ================= EXTENSIONS =================
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    CORS(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # ================= IMPORT MODELS =================
    from models.user import User
    from models.product import Product
    from models.batch import Batch
    from models.scan_log import ScanLog

    # ================= USER LOADER =================
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))  # versi terbaru

    # ================= REGISTER BLUEPRINT =================
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.product import product_bp
    from routes.qr import qr_bp
    from routes.public import public_bp

    app.register_blueprint(auth_bp,      url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(product_bp,   url_prefix='/product')
    app.register_blueprint(qr_bp,        url_prefix='/qr')
    app.register_blueprint(public_bp,    url_prefix='/')

    # ================= GLOBAL VARIABLE =================
    @app.context_processor
    def inject_today():
        return dict(today=date.today())

    # ================= ERROR HANDLER =================
    from sqlalchemy.exc import IntegrityError

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(e):
        return "Data sudah ada (duplikat)!", 400

    # Optional: 404 page
    @app.errorhandler(404)
    def not_found(e):
        return "Halaman tidak ditemukan!", 404

    return app
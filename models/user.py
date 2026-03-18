from app import db, bcrypt
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(120), nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    password   = db.Column(db.String(255), nullable=False)
    plan       = db.Column(db.Enum("free", "pro", "business"), default="free")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    products   = db.relationship("Product", backref="owner", lazy=True)

    def set_password(self, raw):
        self.password = bcrypt.generate_password_hash(raw).decode("utf-8")

    def check_password(self, raw):
        return bcrypt.check_password_hash(self.password, raw)

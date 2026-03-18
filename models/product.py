from app import db
from datetime import datetime
import json

class Product(db.Model):
    __tablename__ = "products"
    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name         = db.Column(db.String(200), nullable=False)
    category     = db.Column(db.String(100))
    description  = db.Column(db.Text)
    custom_fields_schema = db.Column(db.Text)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at   = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    batches      = db.relationship("Batch", backref="product", lazy=True, cascade="all, delete-orphan")

    @property
    def fields_schema(self):
        return json.loads(self.custom_fields_schema) if self.custom_fields_schema else []

    @fields_schema.setter
    def fields_schema(self, value):
        self.custom_fields_schema = json.dumps(value)

from app import db
from datetime import datetime
import json, uuid

class Batch(db.Model):
    __tablename__ = "batches"
    id              = db.Column(db.Integer, primary_key=True)
    product_id      = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    batch_code      = db.Column(db.String(50), unique=True, nullable=False)
    qr_token        = db.Column(db.String(64), unique=True, nullable=False, default=lambda: uuid.uuid4().hex)
    qr_image_path   = db.Column(db.String(255))
    field_data      = db.Column(db.Text)
    production_date = db.Column(db.Date)
    expiry_date     = db.Column(db.Date)
    is_active       = db.Column(db.Boolean, default=True)
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at      = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    scan_logs       = db.relationship("ScanLog", backref="batch", lazy=True, cascade="all, delete-orphan")

    @property
    def data(self):
        return json.loads(self.field_data) if self.field_data else {}

    @data.setter
    def data(self, value):
        self.field_data = json.dumps(value)

    @property
    def total_scans(self):
        return len(self.scan_logs)

from app import db
from datetime import datetime

class ScanLog(db.Model):
    __tablename__ = "scan_logs"
    id         = db.Column(db.Integer, primary_key=True)
    batch_id   = db.Column(db.Integer, db.ForeignKey("batches.id"), nullable=False)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))
    city       = db.Column(db.String(100))
    scanned_at = db.Column(db.DateTime, default=datetime.utcnow)

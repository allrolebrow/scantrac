from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.product import Product
from models.scan_log import ScanLog
from models.batch import Batch
from app import db
from sqlalchemy import func
from datetime import datetime, timedelta

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
@login_required
def index():
    products      = Product.query.filter_by(user_id=current_user.id).all()
    total_batches = Batch.query.join(Product).filter(Product.user_id == current_user.id).count()

    # Total scans across all user batches
    total_scans = (
        db.session.query(func.count(ScanLog.id))
        .join(Batch)
        .join(Product)
        .filter(Product.user_id == current_user.id)
        .scalar() or 0
    )

    # Scans last 7 days
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_scans = (
        db.session.query(func.date(ScanLog.scanned_at), func.count(ScanLog.id))
        .join(Batch).join(Product)
        .filter(Product.user_id == current_user.id, ScanLog.scanned_at >= week_ago)
        .group_by(func.date(ScanLog.scanned_at))
        .all()
    )

    return render_template("dashboard/index.html",
        products=products,
        total_batches=total_batches,
        total_scans=total_scans,
        recent_scans=recent_scans,
    )

from flask import Blueprint, render_template, request
from models.batch import Batch
from models.scan_log import ScanLog
from app import db
from datetime import date  # ✅ tambah ini

public_bp = Blueprint("public", __name__)

@public_bp.route("/")
def landing():
    return render_template("landing.html")

@public_bp.route("/scan/<string:token>")
def scan_product(token):
    batch = Batch.query.filter_by(qr_token=token, is_active=True).first_or_404()

    # Log this scan
    log = ScanLog(
        batch_id=batch.id,
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string[:255],
    )
    db.session.add(log)
    db.session.commit()

    return render_template(
        "public/product_detail.html",
        batch=batch,
        product=batch.product,
        today=date.today()   # ✅ FIX ERROR DI SINI
    )
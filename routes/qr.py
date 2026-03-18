from flask import Blueprint, render_template, redirect, url_for, request, flash, send_file, current_app
from flask_login import login_required, current_user
from models.product import Product
from models.batch import Batch
from app import db
from utils.qr_generator import generate_qr
import uuid, json, os
from datetime import date

qr_bp = Blueprint("qr", __name__)

@qr_bp.route("/batch/new/<int:product_id>", methods=["GET", "POST"])
@login_required
def new_batch(product_id):
    product = Product.query.filter_by(id=product_id, user_id=current_user.id).first_or_404()
    if request.method == "POST":
        batch_code = request.form.get("batch_code", "").strip()
        prod_date  = request.form.get("production_date") or None
        exp_date   = request.form.get("expiry_date") or None

        # collect dynamic field values
        field_data = {}
        for field in product.fields_schema:
            key = field["key"]
            field_data[key] = request.form.get(f"field_{key}", "")

        batch = Batch(
            product_id=product_id,
            batch_code=batch_code,
            qr_token=uuid.uuid4().hex,
        )
        batch.data = field_data
        if prod_date:
            from datetime import datetime
            batch.production_date = datetime.strptime(prod_date, "%Y-%m-%d").date()
        if exp_date:
            from datetime import datetime
            batch.expiry_date = datetime.strptime(exp_date, "%Y-%m-%d").date()

        db.session.add(batch)
        db.session.flush()  # get id before commit

        # Generate QR image
        qr_folder = current_app.config["QR_FOLDER"]
        base_url  = current_app.config["BASE_URL"]
        filename  = generate_qr(batch.qr_token, qr_folder, base_url)
        batch.qr_image_path = filename

        db.session.commit()
        flash("Batch & QR Code berhasil dibuat!", "success")
        return redirect(url_for("qr.view_batch", batch_id=batch.id))
    return render_template("qr/new_batch.html", product=product)

@qr_bp.route("/batch/<int:batch_id>")
@login_required
def view_batch(batch_id):
    batch = Batch.query.join(Product).filter(
        Batch.id == batch_id,
        Product.user_id == current_user.id
    ).first_or_404()
    return render_template("qr/view_batch.html", batch=batch)

@qr_bp.route("/batch/<int:batch_id>/download")
@login_required
def download_qr(batch_id):
    batch = Batch.query.join(Product).filter(
        Batch.id == batch_id,
        Product.user_id == current_user.id
    ).first_or_404()
    filepath = os.path.join(current_app.config["QR_FOLDER"], batch.qr_image_path)
    return send_file(filepath, as_attachment=True, download_name=f"QR_{batch.batch_code}.png")

from datetime import datetime, date

@qr_bp.context_processor
def inject_now():
    return {'now': datetime.utcnow(), 'today': date.today()}

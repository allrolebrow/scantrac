from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from models.product import Product
from models.batch import Batch
from app import db
import json

product_bp = Blueprint("product", __name__)

CATEGORIES = ["Kopi", "Minuman", "Snack", "Makanan", "Herbal", "Kosmetik", "Lainnya"]

@product_bp.route("/")
@login_required
def list_products():
    products = Product.query.filter_by(user_id=current_user.id).order_by(Product.created_at.desc()).all()
    return render_template("product/list.html", products=products)

@product_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_product():
    if request.method == "POST":
        name        = request.form.get("name", "").strip()
        category    = request.form.get("category", "")
        description = request.form.get("description", "")
        # custom fields: sent as JSON string from JS
        fields_json = request.form.get("custom_fields", "[]")
        try:
            fields = json.loads(fields_json)
        except Exception:
            fields = []
        product = Product(
            user_id=current_user.id,
            name=name,
            category=category,
            description=description,
        )
        product.fields_schema = fields
        db.session.add(product)
        db.session.commit()
        flash(f"Produk '{name}' berhasil dibuat!", "success")
        return redirect(url_for("product.list_products"))
    return render_template("product/new.html", categories=CATEGORIES)

@product_bp.route("/<int:product_id>/edit", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    product = Product.query.filter_by(id=product_id, user_id=current_user.id).first_or_404()
    if request.method == "POST":
        product.name        = request.form.get("name", product.name).strip()
        product.category    = request.form.get("category", product.category)
        product.description = request.form.get("description", product.description)
        fields_json = request.form.get("custom_fields", "[]")
        try:
            product.fields_schema = json.loads(fields_json)
        except Exception:
            pass
        db.session.commit()
        flash("Produk berhasil diperbarui.", "success")
        return redirect(url_for("product.list_products"))
    return render_template("product/edit.html", product=product, categories=CATEGORIES)

@product_bp.route("/<int:product_id>/delete", methods=["POST"])
@login_required
def delete_product(product_id):
    product = Product.query.filter_by(id=product_id, user_id=current_user.id).first_or_404()
    db.session.delete(product)
    db.session.commit()
    flash("Produk dihapus.", "info")
    return redirect(url_for("product.list_products"))

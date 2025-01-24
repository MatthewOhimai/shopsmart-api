from flask import request, jsonify
from . import photo_bp
from werkzeug.utils import secure_filename
from ..services.file_service import fileService
from uuid6 import uuid7
import os
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from api import db
from api.v1.models import Product

@photo_bp.route("/upload-image/<category>", methods=["POST"])
def upload_image(category):
    """Upload a product image"""

    if 'image' not in request.files:
        return jsonify({
            "error": "Image file not included in the request"
        }), 400

    file = request.files["image"]

    if file.filename == '':
        return jsonify({
            "error": "No file part selected"
        }), 400

    if not fileService.verify_file_extension(file.filename):
        return jsonify({
            "error": "Not a valid file extension"
        }), 400

    unique_filename = f'{category}_{uuid7().hex}{os.path.splitext(file.filename)[1]}'

    try:
        # Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(file, public_id=unique_filename)
        optimize_url, _ = cloudinary_url(unique_filename, fetch_format="auto", quality="auto")

        print("Cloudinary Upload Result:", upload_result)
        print("Optimized URL:", optimize_url)

        # Ensure all required form data is present
        if 'name' not in request.form or 'new_price' not in request.form:
            return jsonify({
                "error": "Missing required form data"
            }), 400

        # Create Product instance
        new_product = Product(
            name=request.form['name'],
            category=category,
            section=request.form.get('section'),
            image_url=optimize_url,
            new_price=request.form.get('new_price'),
            old_price=request.form.get('old_price')
        )

        print("Product Data:", new_product.__dict__)

        # Save to the database
        db.session.add(new_product)
        try:
            db.session.commit()
        except Exception as e:
            print(f"Database commit error: {e}")
            return jsonify({"error": "Failed to save product to the database"}), 500

        return jsonify({
            "message": "Uploaded successfully",
            "image_url": optimize_url,
            "status": 201,
            "product": new_product.to_dict()
        }), 201

    except Exception as e:
        print(f"Exception in upload_image: {e}")
        return jsonify({
            "error": f"Failed to upload image: {str(e)}"
        }), 500
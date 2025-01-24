from flask import Blueprint, jsonify, request
from flasgger.utils import swag_from
from ..services.product_service import productService
from ..schemas.product_schema import validate_product_input

product_bp = Blueprint('products', __name__)

@product_bp.route("/products", methods=["POST"])
@swag_from('./documentation/product.yml')
def create_product():
	"""Create a new product"""
	data = request.json
	errors, status = validate_product_input(data)
	if status == 400:
		return jsonify({
			"message": "Invalid input. Please check your data.",
			"status_code": status,
			"errors": errors
		}), status

	# Validate image_url
	image_url = data.get("image_url")
	if not image_url:
		return jsonify({
			"message": "Image URL is required.",
			"status_code": 400
		}), 400

	product, status_code = productService.create(data)
	return jsonify({
		"message": "Product created successfully",
		"status_code": status_code,
		"data": {
			**product.to_dict(),
			"image_url": product.image_url  # Use a consistent key
		}
	}), status_code

@product_bp.route("/products", methods=["GET"])
def get_products():
    """Get all products"""
    try:
        products_response, status_code = productService.fetch_all()
        print(f"Products fetched: {products_response}")  # Debugging
        
        if status_code == 200:
            return jsonify(products_response), 200
        else:
            return jsonify(products_response), status_code
    except Exception as e:
        return jsonify({
            "message": "An error occurred while retrieving products.",
            "status_code": 500,
            "error": str(e)
        }), 500

@product_bp.route("/products/<product_id>", methods=["GET"])
def get_product(product_id):
	"""Get a product by ID"""
	product, status_code = productService.fetch_by_id(product_id)
	if status_code == 200:
		return jsonify(product.to_dict()), status_code
	else:
		return jsonify(product), status_code

@product_bp.route("/products/<product_id>", methods=["DELETE"])
def delete_product(product_id):
	"""Delete a product by ID"""
	message, status_code = productService.delete(product_id)
	if status_code == 200:
		return jsonify(message), status_code
	else:
		return jsonify(message), status_code
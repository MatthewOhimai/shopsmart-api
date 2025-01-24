from ..models.product import Product
from api import db
from .service import Service
import cloudinary.uploader
from marshmallow import ValidationError, EXCLUDE
from ..schemas.product_schema import ProductSchema
import logging

logger = logging.getLogger(__name__)

class ProductService(Service):
	def create(self, data):
		try:
			# Validate input
			validated_data = ProductSchema().load(data)

			# Handle image upload
			image = data.get('image')
			if not image:
				return {"message": "Image is required"}, 400

			try:
				upload_result = cloudinary.uploader.upload(image, folder="products")
				image_url = upload_result.get("secure_url")
			except Exception as e:
				logger.error(f"Cloudinary upload error: {e}")
				return {"message": f"Failed to upload image: {str(e)}"}, 500

			# Create and save product
			product = Product(
				name=validated_data['name'],
				category=validated_data['category'],
				image_url=image_url,
				new_price=validated_data['new_price'],
				old_price=validated_data.get('old_price'),
				section=validated_data.get('section', 'product')
			)
			db.session.add(product)
			db.session.commit()
			return product, 201
		except ValidationError as err:
			return {"errors": err.messages, "message": "Validation failed"}, 400
		except Exception as e:
			db.session.rollback()
			logger.error(f"Error creating product: {e}")
			return {"message": f"Failed to create product: {str(e)}"}, 500

	def fetch_all(self):
		try:
			products = Product.query.all()
			if not products:
				return {"message": "No products found", "data": [], "status_code": 404}, 404
			# Ensure that each product is converted to a dict using to_dict()
			return {
				"data": [product.to_dict() for product in products],
				"message": "Products retrieved successfully",
				"status_code": 200
			}, 200
		except Exception as e:
			logger.error(f"Error fetching products: {e}")
			return {"message": "An error occurred while retrieving products.", "status_code": 500, "error": str(e)}, 500

	def fetch_by_id(self, product_id):
		try:
			product = Product.query.get(product_id)
			if not product:
				return None, 404
			return product, 200
		except Exception as e:
			logger.error(f"Error fetching product by ID: {e}")
			return None, 500

	def delete(self, product_id):
		product, status = self.fetch_by_id(product_id)
		if status == 200:
			try:
				db.session.delete(product)
				db.session.commit()
				return {"message": "Product deleted successfully"}, 200
			except Exception as e:
				db.session.rollback()
				logger.error(f"Error deleting product: {e}")
				return {"message": f"Failed to delete product: {str(e)}"}, 500
		return {"message": f"No product with the id: {product_id} found"}, 404

	def update(self, product_id, data):
		product, status = self.fetch_by_id(product_id)
		if status != 200:
			return {"message": "Product not found"}, 404

		try:
			# Validate and update fields
			validated_data = ProductSchema().load(data, partial=True, unknown=EXCLUDE)
			for key, value in validated_data.items():
				setattr(product, key, value)

			# Handle image updates
			if 'image' in data:
				try:
					upload_result = cloudinary.uploader.upload(data['image'], folder="products")
					product.image_url = upload_result.get("secure_url")
				except Exception as e:
					logger.error(f"Error uploading updated image: {e}")
					return {"message": f"Failed to upload image: {str(e)}"}, 500

			db.session.commit()
			return product, 200
		except ValidationError as err:
			return {"errors": err.messages, "message": "Validation failed"}, 400
		except Exception as e:
			db.session.rollback()
			logger.error(f"Error updating product: {e}")
			return {"message": f"Failed to update product: {str(e)}"}, 500

productService = ProductService()
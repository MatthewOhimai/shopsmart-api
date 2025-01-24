from marshmallow import Schema, fields, ValidationError

class ProductSchema(Schema):
	name = fields.Str(required=True, error_messages={"required": "Name is required."})
	category = fields.Str(required=True, error_messages={"required": "Category is required."})
	section = fields.Str(required=False, missing="product")
	image_url = fields.Url(required=False, error_messages={"invalid": "Invalid URL format."})
	new_price = fields.Float(required=True, error_messages={"required": "New price is required."})
	old_price = fields.Float(required=False)

def validate_product_input(data):
	schema = ProductSchema()
	try:
		# Load and validate the input data
		loaded_data = schema.load(data)
		return loaded_data, 200
	except ValidationError as err:
		# Return validation errors with consistent structure
		return {
			"errors": err.messages,
			"message": "Validation failed"
		}, 400
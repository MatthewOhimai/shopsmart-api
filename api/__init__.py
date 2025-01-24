from flask import Flask
from api.extensions import swagger, db, migrate, cors, jwt
from api.v1.routes import main_bp, auth_bp, error_bp, photo_bp
from .v1.routes.photo import photo_bp  # Import the blueprint
from api.v1.routes.product import product_bp
from api.v1.routes.cart_routes import cart_bp
from api.v1.routes.order_routes import order_bp
from config import config

def create_app(env_name):
	"""Flask Application factory function
	
	Args:
		env_name (str): The configuration environment name (e.g., 'development', 'production').

	Returns:
		Flask: Configured Flask application instance.
	"""
	app = Flask(__name__)
	
	# Load configuration from config class
	app.config.from_object(config.get(env_name))

	# Initialize extensions
	swagger.init_app(app)
	db.init_app(app)
	migrate.init_app(app, db)
	cors.init_app(app)
	jwt.init_app(app)

	# Application blueprints with URL prefix
	url_prefix = "/api/v1"
	app.register_blueprint(main_bp, url_prefix=url_prefix)
	app.register_blueprint(auth_bp, url_prefix=url_prefix)
	app.register_blueprint(photo_bp, url_prefix=url_prefix)
	app.register_blueprint(product_bp, url_prefix=url_prefix)
	app.register_blueprint(error_bp)
	app.register_blueprint(cart_bp, url_prefix=url_prefix)
	app.register_blueprint(order_bp, url_prefix=url_prefix)

	return app
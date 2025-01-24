from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests
import cloudinary

# Load environment variables
load_dotenv()

# Environment variables with defaults
DB_ENGINE = os.getenv("DB_ENGINE", "sqlite")
DB_NAME = os.getenv("DB_NAME", "database.db")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
CLOUDINARY_NAME = os.getenv("CLOUDINARY_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
PAYSTACK_PUBLIC_KEY = os.getenv("PAYSTACK_PUBLIC_KEY")
PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")

# Validate essential keys
required_keys = {"JWT_SECRET_KEY": JWT_SECRET_KEY, "SECRET_KEY": SECRET_KEY}
missing_keys = [key for key, value in required_keys.items() if not value]

if missing_keys:
	raise RuntimeError(f"Missing required environment variables: {', '.join(missing_keys)}")

# Cloudinary configuration
if all([CLOUDINARY_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET]):
	cloudinary.config(
		cloud_name=CLOUDINARY_NAME,
		api_key=CLOUDINARY_API_KEY,
		api_secret=CLOUDINARY_API_SECRET,
		secure=True
	)
else:
	print("Warning: Cloudinary configuration is incomplete.")

# Database URI configuration
DATABASE_URIS = {
	"sqlite": f"sqlite:///{DB_NAME}",
	# Extend with other DB engines if needed
}
SQLALCHEMY_DATABASE_URI = DATABASE_URIS.get(DB_ENGINE, DATABASE_URIS["sqlite"])

# Base Configuration
class Config:
	SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	JWT_SECRET_KEY = JWT_SECRET_KEY
	SECRET_KEY = SECRET_KEY
	SWAGGER = {
		"title": "ShopSmart E-Commerce Restful API",
		"uiversion": 3
	}

# Development Configuration
class DevelopmentConfig(Config):
	DEBUG = True

# Configurations dictionary
config = {
	"development": DevelopmentConfig,
	"default": DevelopmentConfig
}

# Paystack Integration Class
class Paystack:
	def __init__(self):
		self.secret_key = PAYSTACK_SECRET_KEY
		self.base_url = "https://api.paystack.co"
		self.headers = {
			"Authorization": f"Bearer {self.secret_key}",
			"Content-Type": "application/json"
		}

	def initialize_payment(self, email, amount):
		"""
		Initialize a payment session with Paystack.
		"""
		data = {"email": email, "amount": int(amount)}
		try:
			response = requests.post(f"{self.base_url}/transaction/initialize", json=data, headers=self.headers)
			response.raise_for_status()
			return response.json()
		except requests.exceptions.RequestException as e:
			print(f"Paystack initialization error: {e}")
			return {"error": "Payment initialization failed"}

	def verify_payment(self, reference):
		"""
		Verify the payment status using Paystack.
		"""
		try:
			response = requests.get(f"{self.base_url}/transaction/verify/{reference}", headers=self.headers)
			response.raise_for_status()
			return response.json()
		except requests.exceptions.RequestException as e:
			print(f"Paystack verification error: {e}")
			return {"error": "Payment verification failed"}

# Flask Application Setup
app = Flask(__name__)
CORS(app)

paystack = Paystack() if PAYSTACK_SECRET_KEY else None

@app.route('/api/v1/payments', methods=['POST'])
def initialize_payment():
	"""
	Route to initialize a payment with Paystack.
	"""
	if not paystack:
		return jsonify({"error": "Paystack integration is not configured properly"}), 500

	data = request.get_json()
	email = data.get("email")
	amount = data.get("amount")

	if not email or not amount:
		return jsonify({"error": "Email and amount are required"}), 400

	if amount <= 0:
		return jsonify({"error": "Amount must be greater than zero"}), 400

	response = paystack.initialize_payment(email, amount)
	if "error" in response:
		return jsonify({"error": response["error"]}), 400

	if response.get("status") == "success":
		return jsonify({
			"status": "success",
			"authorization_url": response["data"]["authorization_url"],
			"reference": response["data"]["reference"]
		}), 200

	return jsonify({"error": "Failed to initialize payment"}), 400

@app.route('/api/v1/payments/verify/<reference>', methods=['GET'])
def verify_payment(reference):
	"""
	Route to verify a payment with Paystack.
	"""
	if not paystack:
		return jsonify({"error": "Paystack integration is not configured properly"}), 500

	response = paystack.verify_payment(reference)
	if "error" in response:
		return jsonify({"error": response["error"]}), 400

	if response.get("status") == "success":
		payment_data = response.get("data", {})
		return jsonify({
			"status": "success",
			"payment_status": payment_data.get("status"),
			"amount": payment_data.get("amount"),
			"email": payment_data.get("customer", {}).get("email"),
			"reference": payment_data.get("reference")
		}), 200

	return jsonify({"error": "Payment verification failed"}), 400

if __name__ == "__main__":
	app.run(debug=True)
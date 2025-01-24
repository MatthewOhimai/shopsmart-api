from api import db
from .base_model import BaseModel

class Product(db.Model):
    __tablename__ = 'products'  # Explicitly set the table name
    # Your fields here
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    category = db.Column(db.String(128), nullable=False)
    image_url = db.Column(db.String(256), nullable=False)
    new_price = db.Column(db.Float, nullable=False)
    old_price = db.Column(db.Float, nullable=True)
    section = db.Column(db.String(128), nullable=False)
    
    def to_dict(self):
     return {
        'id': self.id,
        'name': self.name,
        'category': self.category,
        'image_url': self.image_url,
        'new_price': self.new_price,
        'old_price': self.old_price,
        'section': self.section
    }
     
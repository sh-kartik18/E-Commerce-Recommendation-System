from . import db  
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to the Interactions table
    interactions = db.relationship('Interactions', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    Brand = db.Column(db.String(100))
    Tags = db.Column(db.Text)
    ImageURL = db.Column(db.Text)
    Rating = db.Column(db.Float)
    ReviewCount = db.Column(db.Integer)
    
    # Relationship to the Interactions table
    interactions = db.relationship('Interactions', backref='product', lazy=True)

    def __repr__(self):
        return f'<Product {self.Name}>'

class Interactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float)
    event_type = db.Column(db.String(50)) # e.g., 'click', 'purchase', 'rating'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        return f'<Interaction user:{self.user_id} product:{self.product_id}>'
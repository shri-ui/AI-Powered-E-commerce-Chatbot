from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# Initialize the database
db = SQLAlchemy()

def init_app(app: Flask):
    """Initialize the app with the database."""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Change this for your database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

# Example model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))
    description = db.Column(db.String(200))

    def __repr__(self):
        return f'<Product {self.name}>'

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    browsing_history = db.Column(db.Text)  # Store as JSON string
    past_purchases = db.Column(db.Text)  # Store as JSON string

    def __repr__(self):
        return f'<User {self.name}>' 
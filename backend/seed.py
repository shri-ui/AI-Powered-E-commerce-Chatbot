from app import app
from database import db
from models import Product  # Import your Product model


def seed_data():
    products = [
        Product(name='Red Dress', description='A beautiful red dress.', price=49.99, category='Clothing'),
        Product(name='Blue Sneakers', description='Comfortable blue sneakers.', price=59.99, category='Footwear'),
        Product(name='Smartphone', description='Latest model smartphone.', price=699.99, category='Electronics'),
    ]

    with app.app_context():  # Use application context
        db.session.bulk_save_objects(products)
        db.session.commit()  # Commit the session
        print("Products seeded successfully.")

if __name__ == '__main__':
    seed_data()
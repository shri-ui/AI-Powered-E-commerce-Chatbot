from app import app
from database import db

with app.app_context():
    db.drop_all()  # This will drop all tables
    db.create_all()  # This will create the tables again

print("Database has been reset.") 
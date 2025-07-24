from database import db  # Change to absolute import

class Product(db.Model):
    __tablename__ = 'product'  # Specify the table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=True) 

    __table_args__ = {'extend_existing': True}  # Add this line

    def __repr__(self):
        return f'<Product {self.name}>'

class User(db.Model):
    __tablename__ = 'user'  # Specify the table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    browsing_history = db.Column(db.Text)  # Store as JSON string
    past_purchases = db.Column(db.Text)  # Store as JSON string

    __table_args__ = {'extend_existing': True}  # Add this line

    def __repr__(self):
        return f'<User {self.name}>'

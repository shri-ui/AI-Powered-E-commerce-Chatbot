# app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
from transformers import pipeline
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from database import Product, db, init_app
from chatbot import chat

app = Flask(__name__, static_folder='../frontend/build/static', template_folder='../frontend/build')
CORS(app)

# Redis configuration
redis_client = Redis(host='localhost', port=6379, db=0)

# Define your intent mapping based on your CSV data
intent_mapping = {
    'LABEL_0': 'customer_support',
    'LABEL_1': 'technical_support',
    'LABEL_2': 'greeting',
    'LABEL_3': 'order_status',
    'LABEL_4': 'product_inquiry',
    'LABEL_5': 'shipping',
    'LABEL_6': 'payment',
    'LABEL_7': 'promotions',
    'LABEL_8': 'account_management',
    'LABEL_9': 'product_reviews',
    'LABEL_10': 'feedback',
    'LABEL_11': 'farewell'
}

nlp = pipeline("text-classification", model="bert-base-uncased")

@app.route('/')
def home():
    return send_from_directory(app.template_folder, 'index.html')

@app.route('/favicon.ico')
def favicon():
    return '', 204  # No content, but a valid response

@app.route('/api/products', methods=['GET'])
def get_products():
    # Check Redis cache first
    cached_products = redis_client.get('products')
    if cached_products:
        return jsonify(eval(cached_products))  # Convert string back to list

    # If not cached, fetch from database
    products = Product.query.all()
    products_list = [{'id': p.id, 'name': p.name, 'description': p.description, 'price': p.price, 'category': p.category} for p in products]
    
    # Cache the result
    redis_client.setex('products', 3600, str(products_list))  # Cache for 1 hour
    return jsonify(products_list)

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    user_message = request.json.get('message')
    response = chat(user_message)
    return jsonify({'reply': response})

# Example function to get product embeddings (dummy implementation)
def get_product_embeddings():
    # This should return actual embeddings for your products
    return np.random.rand(3, 768)

@app.route('/api/search', methods=['POST'])
def search():
    query = request.json.get('query')
    query_embedding = np.random.rand(1, 768)  # Replace with actual query embedding
    product_embeddings = get_product_embeddings()
    similarities = cosine_similarity(query_embedding, product_embeddings)
    best_match_index = np.argmax(similarities)
    return jsonify({'best_match': best_match_index})

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

# Create database tables within application context
with app.app_context():
    init_app(app)  # Initialize the app with the database
    db.create_all()  # Create database tables

if __name__ == '__main__':
    app.run(debug=True)
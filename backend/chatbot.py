from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import pickle
import re

# Load the trained model, tokenizer, and label encoder
model_path = "backend/models/my_model"
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Load the label encoder
with open(f"{model_path}/label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

def preprocess_text(text):
    """Preprocess the input text to handle various cases"""
    text = text.lower().strip()
    
    if len(text.split()) == 1:
        keyword_mapping = {
            # Customer Support
            'support': 'I need customer support',
            'help': 'I need customer support help',
            
            # Technical Support
            'technical': 'I need technical support',
            'device': 'Having issues with my device',
            
            # Order Status
            'order': 'Where is my order',
            'track': 'Track my order',
            'status': 'Order status',
            
            # Product Inquiry
            'product': 'Show me products',
            'products': 'What products do you have',
            
            # Shipping
            'shipping': 'What\'s the shipping cost?',
            'delivery': 'When will my order arrive?',
            
            # Payment
            'payment': 'What payment methods do you accept?',
            'pay': 'How can I pay for my order?',
            
            # Promotions
            'deals': 'Are there any deals today?',
            'sale': 'What\'s on sale?',
            'discount': 'Any discount available?',
            
            # Account Management
            'account': 'Need to update my profile',
            'password': 'How do I change my password?',
            'login': 'Can\'t login to my account',
            
            # Reviews
            'review': 'How can I rate the product?',
            'reviews': 'Where are the customer reviews?',
            'rating': 'Show me product ratings',
            
            # Feedback
            'feedback': 'Want to leave feedback',
            
            # Greetings
            'hello': 'Hello',
            'hi': 'Hi there',
            'hey': 'Hey',
            
            # Farewell
            'bye': 'Goodbye',
            'goodbye': 'Goodbye',
            'thanks': 'Thanks, bye'
        }
        return keyword_mapping.get(text, text)
    
    return text

def chat(user_message):
    # Preprocess the input message
    processed_message = preprocess_text(user_message)
    lower_message = user_message.lower().strip()
    
    # Handle order status queries specifically
    order_keywords = ['where', 'track', 'status', 'my order', 'find order']
    if any(keyword in lower_message for keyword in order_keywords):
        return intent_responses["order_status"]["high_conf"]
    
    # Handle single word inputs with precise matching
    if len(lower_message.split()) == 1:
        # Farewell words
        if lower_message in ['bye', 'goodbye']:
            return intent_responses["farewell"]["high_conf"]
            
        # Greeting words
        if lower_message in ['hello', 'hi', 'hey']:
            return intent_responses["greeting"]["high_conf"]
            
        # Support related
        if lower_message == 'support':
            return intent_responses["customer_support"]["high_conf"]
        if lower_message == 'technical':
            return intent_responses["technical_support"]["high_conf"]
            
        # Order related
        if lower_message in ['order', 'track', 'status']:
            return intent_responses["order_status"]["high_conf"]
            
        # Product related
        if lower_message in ['product', 'products']:
            return intent_responses["product_inquiry"]["high_conf"]
            
        # Shipping related
        if lower_message in ['shipping', 'delivery']:
            return intent_responses["shipping"]["high_conf"]
            
        # Payment related
        if lower_message in ['payment', 'pay']:
            return intent_responses["payment"]["high_conf"]
            
        # Deals related
        if lower_message in ['deals', 'sale', 'discount']:
            return intent_responses["promotions"]["high_conf"]
            
        # Account related
        if lower_message in ['account', 'password', 'login']:
            return intent_responses["account_management"]["high_conf"]
            
        # Review related
        if lower_message in ['review', 'reviews', 'rating']:
            return intent_responses["product_reviews"]["high_conf"]
            
        # Feedback
        if lower_message == 'feedback':
            return intent_responses["feedback"]["high_conf"]
    
    # Check for common phrases before using model
    if "where is my order" in lower_message:
        return intent_responses["order_status"]["high_conf"]
    
    if "track my order" in lower_message:
        return intent_responses["order_status"]["high_conf"]
    
    if "order status" in lower_message:
        return intent_responses["order_status"]["high_conf"]
    
    if "need help" in lower_message or "can you help" in lower_message:
        return intent_responses["customer_support"]["high_conf"]
    
    if "speak to support" in lower_message or "contact support" in lower_message:
        return intent_responses["customer_support"]["high_conf"]
    
    # For multi-word messages, use the model prediction
    inputs = tokenizer(processed_message, return_tensors="pt", padding=True, truncation=True)
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    predictions = outputs.logits.argmax(dim=-1).item()
    confidence = torch.softmax(outputs.logits, dim=-1)[0].max().item()
    predicted_label = label_encoder.inverse_transform([predictions])[0]

    # For debugging
    print(f"Message: {user_message}")
    print(f"Processed message: {processed_message}")
    print(f"Predicted label: {predicted_label}")
    print(f"Confidence: {confidence}")

    # Get response based on predicted intent
    if predicted_label in intent_responses:
        if confidence >= CONFIDENCE_THRESHOLD:
            return intent_responses[predicted_label]["high_conf"]
        else:
            return intent_responses[predicted_label]["low_conf"]
    
    return "I'm not sure I understand. Could you please rephrase your question?"

# Define your intent responses based on your CSV data
intent_responses = {
    "customer_support": {
        "high_conf": "I'm here to help! What issue can I assist you with today?",
        "low_conf": "It seems you need assistance. Could you please describe your concern?"
    },
    "technical_support": {
        "high_conf": "I'll help you resolve your technical issue. Could you describe the problem you're experiencing?",
        "low_conf": "For technical support, I'll need more details about the problem you're facing."
    },
    "greeting": {
        "high_conf": "Hello! How can I assist you today?",
        "low_conf": "Hi there! How can I help you?"
    },
    "order_status": {
        "high_conf": "Please provide your order number, and I'll check the status for you right away.",
        "low_conf": "I can help you track your order. Could you please share your order number?"
    },
    "product_inquiry": {
        "high_conf": "Sure! Here are some options for the product you're looking for. What specific product interests you?",
        "low_conf": "Are you looking for information about a specific product? Could you provide more details?"
    },
    "shipping": {
        "high_conf": "We offer free shipping on orders over $50. Standard shipping costs $5.99 and takes 3-5 business days.",
        "low_conf": "Would you like to know more about our shipping options and delivery times?"
    },
    "payment": {
        "high_conf": "We accept all major credit cards, PayPal, and Apple Pay. Which payment method would you prefer?",
        "low_conf": "I can help you with payment information. What specific details would you like to know?"
    },
    "promotions": {
        "high_conf": "Yes! We currently have several deals running. Check out our 'Special Offers' section for up to 50% off!",
        "low_conf": "Would you like to know about our current sales and promotions?"
    },
    "account_management": {
        "high_conf": "You can manage your account settings, including password changes, in the 'My Account' section.",
        "low_conf": "I can help you with your account. What specific changes would you like to make?"
    },
    "product_reviews": {
        "high_conf": "You can find product reviews on each product page under the 'Reviews' tab. Would you like to write or read a review?",
        "low_conf": "Are you looking to read or write a product review?"
    },
    "feedback": {
        "high_conf": "We value your feedback! You can leave your comments through our feedback form or customer service.",
        "low_conf": "Would you like to provide feedback about our products or services?"
    },
    "farewell": {
        "high_conf": "Thank you for chatting! Have a great day!",
        "low_conf": "Goodbye! Feel free to come back if you need anything else."
    }
}

# Define threshold for confidence
CONFIDENCE_THRESHOLD = 0.7

def handle_intent(intent_label, confidence, original_message):
    # Base responses
    intent_responses = {
        "product_inquiry": {
            "high_conf": "What specific product would you like to know about?",
            "low_conf": "Are you looking for information about our products? Could you please provide more details?"
        },
        "order_status": {
            "high_conf": "Please provide your order number to check the status.",
            "low_conf": "It seems you're asking about an order. Could you provide more details or your order number?"
        },
        "customer_support": {
            "high_conf": "How can I assist you with customer support today?",
            "low_conf": "I'd be happy to help. Could you please describe your issue in more detail?"
        },
        "greeting": {
            "high_conf": "Hello! How can I assist you today?",
            "low_conf": "Hello! How can I help you?"
        },
        "purchase_intent": {
            "high_conf": "What product would you like to purchase?",
            "low_conf": "Are you interested in buying something? What kind of product are you looking for?"
        }
        # Add more intents and responses as needed
    }

    # Get the appropriate response based on confidence
    if intent_label in intent_responses:
        if confidence >= CONFIDENCE_THRESHOLD:
            return intent_responses[intent_label]["high_conf"]
        else:
            return intent_responses[intent_label]["low_conf"]
    
    # Fallback to keyword-based response if intent recognition fails
    keyword_intent = extract_keywords(original_message)
    if keyword_intent and keyword_intent in intent_responses:
        return intent_responses[keyword_intent]["low_conf"]
    
    return "I'm not sure I understand. Could you please rephrase your question?"

def extract_keywords(text):
    """Extract important keywords from text"""
    # Add more keywords as needed
    keywords = {
        'order': 'order_status',
        'track': 'order_status',
        'status': 'order_status',
        'product': 'product_inquiry',
        'buy': 'product_inquiry',
        'purchase': 'product_inquiry',
        'price': 'product_inquiry',
        'cost': 'product_inquiry',
        'help': 'customer_support',
        'support': 'customer_support',
        'hello': 'greeting',
        'hi': 'greeting',
        'hey': 'greeting'
    }
    
    words = text.lower().split()
    for word in words:
        if word in keywords:
            return keywords[word]
    return None
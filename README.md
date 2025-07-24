
# E-commerce AI Chatbot

An intelligent customer service chatbot built with React and Flask, designed to handle various e-commerce queries including order tracking, product information, and customer support.

## Features

- 🤖 Intelligent intent recognition
- 💬 Modern floating chat interface
- 🎯 Precise query handling
- 📱 Responsive design
- 🛍️ E-commerce focused responses

## Tech Stack

### Frontend
- React.js
- Axios for API calls
- CSS3 with animations
- Responsive design

### Backend
- Flask
- Transformers (Hugging Face)
- PyTorch
- SQLAlchemy
- Flask-CORS

## Quick Start

1. **Clone the repository**
```bash
git clone <https://github.com/shri-ui/AI-Powered-E--commerce-Chatbot-API.git>
cd e-commerce-chatbot
```

2. **Backend Setup**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Train the model
python backend/model_training.py

# Start Flask server
python backend/app.py
```

3. **Frontend Setup**
```bash
cd frontend
npm install
npm start
```

## Project Structure
```
e-commerce-chatbot/
├── backend/
│   ├── app.py              # Flask server
│   ├── chatbot.py          # Chatbot logic
│   ├── model_training.py   # Model training
│   └── e-commerce.csv      # Training data
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── Chatbot.js
│       │   └── Chatbot.css
│       └── App.js
└── requirements.txt
```

## Supported Intents

| Intent | Description | Example Queries |
|--------|-------------|----------------|
| Customer Support | General assistance | "need help", "support" |
| Technical Support | Technical issues | "device not working" |
| Order Status | Order tracking | "where is my order" |
| Product Inquiry | Product information | "show products" |
| Shipping | Shipping information | "shipping cost" |
| Payment | Payment methods | "payment options" |
| Account | Account management | "reset password" |
| Reviews | Product reviews | "show reviews" |

## API Endpoints

### Chat Endpoint
```
POST /api/chat
Request: {"message": "user message"}
Response: {"reply": "bot response"}
```

## Model Training

The chatbot uses a fine-tuned DistilBERT model trained on e-commerce conversations. Training data includes:
- Customer support queries
- Order-related questions
- Product inquiries
- Technical support issues

To retrain the model:
```bash
python backend/model_training.py
```

## Configuration

Key configurations in `backend/chatbot.py`:
```python
CONFIDENCE_THRESHOLD = 0.7  # Confidence threshold for intent detection
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/NewFeature`)
3. Commit changes (`git commit -m 'Add NewFeature'`)
4. Push to branch (`git push origin feature/NewFeature`)
5. Open Pull Request

## Future Enhancements

- [ ] Multi-language support
- [ ] Conversation history
- [ ] User authentication
- [ ] Enhanced response personalization
- [ ] Integration with e-commerce platforms

## License

MIT License - see LICENSE file for details


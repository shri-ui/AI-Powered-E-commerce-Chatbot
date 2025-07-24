// src/components/Chatbot.js
import React, { useState } from 'react';
import './Chatbot.css'; // Import the CSS file
import axios from 'axios';

const Chatbot = () => {
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');
    const [isOpen, setIsOpen] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!inputMessage.trim()) return;

        // Add user message
        const newMessages = [...messages, { text: inputMessage, isUser: true }];
        setMessages(newMessages);

        try {
            // Using your existing axios call
            const response = await axios.post('http://localhost:5000/api/chat', {
                message: inputMessage,
            });
            
            // Add bot response
            setMessages([...newMessages, { text: response.data.reply, isUser: false }]);
            setInputMessage('');
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div className="chatbot-container">
            {/* Floating button */}
            <button 
                className={`chat-toggle-button ${isOpen ? 'open' : ''}`}
                onClick={() => setIsOpen(!isOpen)}
            >
                {isOpen ? '×' : '💬'}
            </button>

            {/* Chat window */}
            {isOpen && (
                <div className="chat-window">
                    <div className="chat-header">
                        <div className="user-info">
                            <img src="/avatar.png" alt="Bot Avatar" className="avatar" />
                            <span className="username">AI Assistant</span>
                        </div>
                        <button 
                            className="close-button"
                            onClick={() => setIsOpen(false)}
                        >
                            ×
                        </button>
                    </div>

                    <div className="messages-container">
                        {messages.map((message, index) => (
                            <div
                                key={index}
                                className={`message ${message.isUser ? 'user-message' : 'bot-message'}`}
                            >
                                {message.text}
                            </div>
                        ))}
                    </div>

                    <form onSubmit={handleSubmit} className="input-container">
                        <input
                            type="text"
                            value={inputMessage}
                            onChange={(e) => setInputMessage(e.target.value)}
                            placeholder="Type a message..."
                            className="message-input"
                        />
                        <button type="submit" className="send-button">
                            <span role="img" aria-label="send">➤</span>
                        </button>
                    </form>
                </div>
            )}
        </div>
    );
};

export default Chatbot;
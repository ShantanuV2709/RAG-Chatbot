# Testing configuration and sample tests for RAG Chatbot

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Tests for health check endpoint."""
    
    def test_health_check(self):
        """Test that health endpoint returns successful response."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        assert "service" in response.json()
        assert "version" in response.json()


class TestRootEndpoint:
    """Tests for root endpoint."""
    
    def test_root(self):
        """Test that root endpoint returns API information."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data
        assert "health" in data


class TestAskEndpoint:
    """Tests for /ask endpoint."""
    
    def test_ask_valid_question(self):
        """Test asking a valid question."""
        payload = {
            "question": "What is your purpose?",
            "chat_history": []
        }
        response = client.post("/ask", json=payload)
        assert response.status_code == 200
        assert "answer" in response.json()
    
    def test_ask_empty_question(self):
        """Test that empty question is rejected."""
        payload = {
            "question": "",
            "chat_history": []
        }
        response = client.post("/ask", json=payload)
        assert response.status_code == 400
    
    def test_ask_with_chat_history(self):
        """Test asking a question with chat history."""
        payload = {
            "question": "What did I just ask?",
            "chat_history": [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there!"}
            ]
        }
        response = client.post("/ask", json=payload)
        assert response.status_code == 200
        assert "answer" in response.json()
    
    def test_ask_question_too_long(self):
        """Test that overly long questions are rejected."""
        payload = {
            "question": "a" * 6000,  # Exceeds 5000 char limit
            "chat_history": []
        }
        response = client.post("/ask", json=payload)
        assert response.status_code == 422  # Validation error


# Run tests with: pytest test_main.py -v

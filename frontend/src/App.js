import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./App.css";
import { FaUser, FaRobot, FaMoon, FaSun, FaDownload, FaTrash } from "react-icons/fa";

function App() {
  const [question, setQuestion] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const chatBoxRef = useRef(null);

  // Toggle body class based on darkMode state
  useEffect(() => {
    document.body.className = darkMode ? "dark" : "light";
  }, [darkMode]);

  // Scroll chat box to bottom whenever chat history or loading state changes
  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTo(0, chatBoxRef.current.scrollHeight);
    }
  }, [chatHistory, loading]);

  // Handle asking question
  const askQuestion = async () => {
    if (!question.trim()) return;

    const timestamp = new Date().toLocaleTimeString();

    // Add user's question to chat history
    setChatHistory((prev) => [
      ...prev,
      { role: "user", content: question, timestamp },
    ]);
    setLoading(true);
    setQuestion(""); // Clear input immediately for better UX

    try {
      const response = await axios.post("http://127.0.0.1:8000/ask", {
        question,
        chat_history: chatHistory,
      });

      const answer = response.data.answer;

      // Add assistant's answer to chat history
      setChatHistory((prev) => [
        ...prev,
        { role: "assistant", content: answer, timestamp: new Date().toLocaleTimeString() },
      ]);
    } catch (error) {
      // Display error in chat UI instead of alert
      let errorMessage = "Sorry, I encountered an error processing your question.";

      if (error.response) {
        // Server responded with error
        errorMessage = error.response.data.detail || `Server error: ${error.response.status}`;
      } else if (error.request) {
        // Request made but no response
        errorMessage = "Unable to connect to the server. Please ensure the backend is running.";
      } else {
        // Something else happened
        errorMessage = `Error: ${error.message}`;
      }

      setChatHistory((prev) => [
        ...prev,
        {
          role: "error",
          content: errorMessage,
          timestamp: new Date().toLocaleTimeString()
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  // Export conversation as text file
  const exportConversation = () => {
    if (chatHistory.length === 0) {
      alert("No conversation to export!");
      return;
    }

    const text = chatHistory
      .map((msg) => {
        const role = msg.role === "user" ? "You" : msg.role === "assistant" ? "Bot" : "Error";
        return `[${msg.timestamp}] ${role}: ${msg.content}`;
      })
      .join("\n\n");

    const blob = new Blob([text], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `chat-${new Date().toISOString().slice(0, 10)}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  // Clear conversation
  const clearConversation = () => {
    if (chatHistory.length === 0) return;
    if (window.confirm("Are you sure you want to clear the conversation?")) {
      setChatHistory([]);
    }
  };

  return (
    <div className="app">
      <header>
        <div>RAG Chatbot</div>
        <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
          <button
            className="icon-button"
            onClick={clearConversation}
            disabled={chatHistory.length === 0}
            title="Clear conversation"
          >
            <FaTrash />
          </button>
          <button
            className="icon-button"
            onClick={exportConversation}
            disabled={chatHistory.length === 0}
            title="Export conversation"
          >
            <FaDownload />
          </button>
          <div
            className="theme-toggle"
            role="button"
            tabIndex={0}
            onClick={() => setDarkMode(!darkMode)}
            onKeyPress={(e) => {
              if (e.key === "Enter") setDarkMode(!darkMode);
            }}
            aria-label="Toggle dark mode"
          >
            {darkMode ? <FaSun /> : <FaMoon />}
          </div>
        </div>
      </header>

      <div className="chat-container">
        <div className="chat-box" ref={chatBoxRef}>
          {chatHistory.map((msg, i) => (
            <div key={i} className={`message ${msg.role}`}>
              <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                {msg.role === "user" ? <FaUser /> : <FaRobot />}
                <span>{msg.content}</span>
              </div>
              <div className="timestamp">{msg.timestamp}</div>
            </div>
          ))}
          {loading && <div className="typing-indicator">Bot is typing...</div>}
        </div>

        <textarea
          rows={3}
          placeholder="Ask your question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              if (!loading) askQuestion();
            }
          }}
          disabled={loading}
        />
        <button onClick={askQuestion} disabled={loading || !question.trim()}>
          {loading ? "Loading..." : "Ask"}
        </button>
      </div>
    </div>
  );
}

export default App;

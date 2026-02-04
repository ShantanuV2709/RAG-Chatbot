# RAG Chatbot 🤖

A Retrieval-Augmented Generation (RAG) chatbot built with FastAPI backend and React frontend, powered by Google's Generative AI.

## Features

- 💬 **Interactive conversational interface** with dark/light mode
- 🔍 **RAG-based responses** using ChromaDB vector store
- 💾 **Persistent embeddings** - saves to disk to avoid API quota exhaustion
- 📚 **Support for PDF and text** document knowledge bases
- ⚙️ **Centralized configuration** with Pydantic Settings validation
- 🌓 **Dark/Light mode toggle** with smooth transitions
- ⚡ **Real-time chat** with conversation history
- 📥 **Export conversations** as text files
- 🗑️ **Clear conversation** with confirmation
- 🎨 **Modern, responsive UI** with error messages in chat
- 🔒 **Environment-based CORS** for security
- 🏥 **Health check endpoints** for monitoring
- 📝 **Comprehensive logging** with configurable levels
- ✅ **Testing infrastructure** with pytest

## Tech Stack

**Backend:**
- FastAPI - Modern web framework
- LangChain - RAG orchestration
- ChromaDB - Vector database
- Google Generative AI - LLM and embeddings
- Python 3.8+

**Frontend:**
- React 19
- Axios - HTTP client
- React Icons
- CSS3 with animations

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- Google AI API Key ([Get one here](https://makersuite.google.com/app/apikey))

## Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows: `venv\\Scripts\\activate`
- macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file (copy from `.env.example`):
```bash
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux
```

6. Edit `.env` and add your Google API key:
```
GOOGLE_API_KEY=your_actual_api_key_here
ALLOWED_ORIGINS=http://localhost:3000
```

7. Add your knowledge documents to the `data/` folder:
- `knowledge.txt` - Text file with information
- `Knowledge.pdf` - PDF document with information

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Running the Application

### Start the Backend

From the `backend` directory:
```bash
uvicorn main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`
- API Documentation: `http://127.0.0.1:8000/docs`
- Health Check: `http://127.0.0.1:8000/health`

### Start the Frontend

From the `frontend` directory:
```bash
npm start
```

The React app will open at: `http://localhost:3000`

## Project Structure

```
RAG-Chatbot/
├── backend/
│   ├── data/              # Knowledge base documents
│   │   ├── knowledge.txt
│   │   └── Knowledge.pdf
│   ├── main.py           # FastAPI application
│   ├── rag_chain.py      # RAG chain setup
│   ├── list_models.py    # Utility to list available models
│   ├── requirements.txt  # Python dependencies
│   ├── .env             # Environment variables (not in git)
│   └── .env.example     # Environment template
├── frontend/
│   ├── src/
│   │   ├── App.js       # Main React component
│   │   ├── App.css      # Styles
│   │   └── index.js     # Entry point
│   ├── public/
│   └── package.json     # Node dependencies
└── README.md
```

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check endpoint
- `POST /ask` - Submit a question
  ```json
  {
    "question": "Your question here",
    "chat_history": []
  }
  ```

## Configuration

### Backend Environment Variables

- `GOOGLE_API_KEY` - **(Required)** Your Google AI API key
- `ALLOWED_ORIGINS` - **(Optional)** Comma-separated allowed CORS origins (default: `http://localhost:3000,http://127.0.0.1:3000`)
- `LOG_LEVEL` - **(Optional)** Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL (default: `INFO`)
- `CHUNK_SIZE` - **(Optional)** Document chunk size for splitting (default: `500`)
- `CHUNK_OVERLAP` - **(Optional)** Overlap between chunks (default: `50`)
- `RETRIEVER_K` - **(Optional)** Number of documents to retrieve (default: `3`)
- `EMBEDDING_MODEL` - **(Optional)** Model for embeddings (default: `models/embedding-001`)
- `LLM_MODEL` - **(Optional)** Model for text generation (default: `models/gemini-1.5-flash`)

### Customization

**Change Chunk Size:**
Edit `.env`:
```bash
CHUNK_SIZE=1000
CHUNK_OVERLAP=100
```

**Change Number of Retrieved Documents:**
Edit `.env`:
```bash
RETRIEVER_K=5
```

**Change LLM Model:**
Edit `.env`:
```bash
LLM_MODEL=models/gemini-1.5-pro
```

**Change Logging Level:**
Edit `.env`:
```bash
LOG_LEVEL=DEBUG
```

## Troubleshooting

### Backend won't start
- Ensure your `.env` file contains a valid `GOOGLE_API_KEY`
- Check that data files exist in `backend/data/`
- Verify Python virtual environment is activated
- Check for import errors - ensure all packages are installed

### Frontend can't connect
- Ensure backend is running on port 8000
- Check CORS configuration in backend `.env`
- Verify no firewall blocking localhost connections

### No responses generated
- Check API key is valid
- Verify documents are loaded (check console output)
- Ensure internet connection for API calls

### API Quota Exceeded Error

**Error:** `429 You exceeded your current quota`

**Solution:** The project now uses **persistent ChromaDB** which saves embeddings to disk:

1. **First run:** Embeddings are created and saved to `backend/chroma_db/` folder
2. **Subsequent runs:** Embeddings load from disk (NO API calls!)
3. **To rebuild embeddings** (after adding new documents):
   ```bash
   cd backend
   Remove-Item -Recurse -Force chroma_db  # Windows
   # rm -rf chroma_db  # Linux/Mac
   ```
   Then restart the server - it will recreate and save embeddings

**Daily quota limits:**
- Free tier has daily limits on embedding requests
- With persistent storage, you only use quota ONCE for initial embedding creation

### Frontend Dependencies Issues

If you get errors about missing packages:
```bash
cd frontend
rm -rf node_modules package-lock.json  # Delete existing
npm install  # Reinstall fresh
```

### Python Import Errors

If you get `ModuleNotFoundError`:
```bash
cd backend
# Activate venv first
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate  # Linux/Mac

# Install missing packages
pip install langchain==0.1.20 langchain-community==0.0.38 langchain-google-genai==0.0.11
pip install fastapi uvicorn chromadb pypdf pydantic-settings python-dotenv
```

## Recent Improvements

### ✅ **Critical Bug Fixes:**
- Fixed API key bug (was using literal string `"API_KEY"` instead of variable) - **completely broke the application**
- Fixed file path case sensitivity (`knowledge.pdf` → `Knowledge.pdf`)
- Added missing axios dependency
- Added comprehensive error handling for missing data files
- Fixed import paths for LangChain v0.3+ compatibility

### ✅ **Performance & Reliability:**
- **Persistent ChromaDB storage** - embeddings saved to disk, prevents API quota exhaustion on every restart
- Centralized configuration management with Pydantic Settings
- Environment-based settings with validation and type checking
- Proper logging infrastructure with configurable levels

### ✅ **Security Enhancements:**
- Environment-based CORS configuration (no longer accepts all origins)
- Input validation with field constraints (1-5000 character limit)
- Proper HTTP error codes and status handling
- API key securely loaded from environment variables

### ✅ **User Experience:**
- **Conversation export** - download chat history as `.txt` file
- **Clear conversation** - with confirmation dialog
- Error messages displayed in chat UI (not generic alerts)
- Better loading states and visual feedback
- Icon buttons with hover effects

### ✅ **Developer Experience:**
- Health check endpoints (`/health`, `/`)
- Comprehensive logging with timestamps
- Testing framework with pytest
- Complete documentation (README, .env.example)
- Improved .gitignore coverage

### ✅ **New Files Added:**
- `backend/config.py` - Centralized configuration module
- `backend/test_main.py` - API endpoint tests
- `backend/.env.example` - Environment variable template
- Comprehensive README with installation & troubleshooting

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please open an issue on GitHub.

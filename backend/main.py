from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from rag_chain import qa_chain
from config import settings
import logging

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RAG Chatbot API",
    description="API for RAG-based conversational AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,  # Use config
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(f"CORS enabled for origins: {settings.origins_list}")

class Query(BaseModel):
    question: str = Field(..., min_length=1, max_length=5000, description="User's question")
    chat_history: List[Dict[str, Any]] = Field(default=[], description="Chat history")

@app.get("/health")
async def health_check():
    """Health check endpoint to verify API is running"""
    return {
        "status": "healthy",
        "service": "RAG Chatbot API",
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "RAG Chatbot API",
        "docs": "/docs",
        "health": "/health"
    }

@app.post("/ask")
async def ask_question(query: Query):
    """Process a question and return an AI-generated answer"""
    try:
        logger.info(f"Received question: {query.question[:100]}...")  # Log first 100 chars
        
        # Validate question
        if not query.question.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Question cannot be empty"
            )
        
        # Prepare input dictionary with keys the chain expects
        input_dict = {
            "question": query.question,
            "chat_history": query.chat_history
        }

        # Call the chain with the input dictionary
        result = qa_chain(input_dict)

        # Extract answer safely
        answer_text = result.get("answer", "No answer found.")
        
        logger.info(f"Successfully generated answer (length: {len(answer_text)} chars)")
        
        return {"answer": answer_text}
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing your question: {str(e)}"
        )

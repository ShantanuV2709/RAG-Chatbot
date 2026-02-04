"""
Configuration management module for RAG Chatbot backend.
Centralizes environment variable loading and validation using Pydantic.
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Required settings
    google_api_key: str
    
    # Optional settings with defaults
    allowed_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    log_level: str = "INFO"
    
    # Data file paths
    data_dir: str = "data"
    txt_file: str = "knowledge.txt"
    pdf_file: str = "Knowledge.pdf"
    
    # RAG configuration
    chunk_size: int = 500
    chunk_overlap: int = 50
    retriever_k: int = 3
    
    # Model configuration
    embedding_model: str = "models/embedding-001"
    llm_model: str = "models/gemini-1.5-flash"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        # Map environment variables to field names
        fields = {
            'google_api_key': {'env': 'GOOGLE_API_KEY'},
            'allowed_origins': {'env': 'ALLOWED_ORIGINS'},
        }
    
    @property
    def txt_file_path(self) -> str:
        """Full path to text knowledge file."""
        return os.path.join(self.data_dir, self.txt_file)
    
    @property
    def pdf_file_path(self) -> str:
        """Full path to PDF knowledge file."""
        return os.path.join(self.data_dir, self.pdf_file)
    
    @property
    def origins_list(self) -> List[str]:
        """Parse allowed origins as a list."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]


# Global settings instance
try:
    settings = Settings()
except Exception as e:
    print(f"❌ Configuration Error: {e}")
    print("Please ensure your .env file contains all required variables.")
    print("See .env.example for reference.")
    raise

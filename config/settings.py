"""
Configuration settings for PDF Chat RAG application.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application configuration settings."""
    
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    LLM_MODEL: str = "llama-3.3-70b-versatile"
    LLM_TEMPERATURE: float = 0.2
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    PAGE_TITLE: str = "Chat with PDFs (Groq)"
    PAGE_ICON: str = "📚"
    
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    
    @classmethod
    def validate(cls) -> None:
        """Validate required configuration."""
        if not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY environment variable is required")


settings = Settings()

"""
Logging configuration and utilities.
"""
import logging
import warnings
from config.settings import settings


def setup_logging() -> logging.Logger:
    """
    Configure application logging.
    
    Returns:
        logging.Logger: Configured logger instance
    """
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format=settings.LOG_FORMAT,
        handlers=[logging.StreamHandler()]
    )
    
    warnings.filterwarnings("ignore")
    logging.getLogger("PyPDF2").setLevel(logging.ERROR)
    logging.getLogger("pypdf").setLevel(logging.ERROR)
    logging.getLogger("pypdf._reader").setLevel(logging.ERROR)
    logging.getLogger("httpx").setLevel(logging.ERROR)
    logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
    logging.getLogger("transformers").setLevel(logging.ERROR)
    logging.getLogger("torch").setLevel(logging.ERROR)
    logging.getLogger("faiss").setLevel(logging.ERROR)
    logging.getLogger("urllib3").setLevel(logging.ERROR)
    
    return logging.getLogger(__name__)


logger = setup_logging()
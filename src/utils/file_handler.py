"""
File handling utilities.
"""
import os
import tempfile
from typing import BinaryIO
from src.utils.logger import logger


def save_uploaded_file(uploaded_file: BinaryIO, filename: str) -> str:
    """
    Save uploaded file to temporary directory.
    
    Args:
        uploaded_file: File-like object from Streamlit uploader
        filename: Original filename
        
    Returns:
        str: Path to saved temporary file
    """
    temp_path = os.path.join(tempfile.gettempdir(), filename)
    
    try:
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())
        return temp_path
    except Exception as e:
        logger.error(f"Error saving file {filename}: {str(e)}")
        raise


def cleanup_temp_file(filepath: str) -> None:
    """
    Remove temporary file if it exists.
    
    Args:
        filepath: Path to file to remove
    """
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception as e:
        logger.warning(f"Could not clean up temp file: {str(e)}")
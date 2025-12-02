"""
Vector store service for document embeddings and retrieval.
"""
from typing import List
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document

from config.settings import settings
from src.utils.logger import logger


class VectorStoreService:
    """Manage vector store operations."""
    
    def __init__(self, model_name: str = settings.EMBEDDING_MODEL):
        """
        Initialize vector store service.
        
        Args:
            model_name: Name of the embedding model
        """
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={"device": "cpu"}
        )
        logger.info(f"Loaded embedding model: {model_name.split('/')[-1]}")
    
    def create_vectorstore(self, chunks: List[Document]) -> FAISS:
        """
        Create FAISS vector store from document chunks.
        
        Args:
            chunks: List of document chunks
            
        Returns:
            FAISS: Vector store instance
        """
        try:
            vectorstore = FAISS.from_documents(
                documents=chunks,
                embedding=self.embeddings
            )
            logger.info(f"Vector store created successfully")
            return vectorstore
        except Exception as e:
            logger.error(f"Error creating vector store: {str(e)}")
            raise
    
    def get_retriever(self, vectorstore: FAISS, k: int = 4):
        """
        Get retriever from vector store.
        
        Args:
            vectorstore: FAISS vector store
            k: Number of documents to retrieve
            
        Returns:
            Retriever instance
        """
        return vectorstore.as_retriever(search_kwargs={"k": k})
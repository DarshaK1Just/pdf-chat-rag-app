"""
PDF processing service for document extraction and chunking.
"""
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

from config.settings import settings
from src.utils.file_handler import save_uploaded_file
from src.utils.logger import logger


class PDFProcessor:
    """Handle PDF document processing operations."""
    
    def __init__(
        self,
        chunk_size: int = settings.CHUNK_SIZE,
        chunk_overlap: int = settings.CHUNK_OVERLAP
    ):
        """
        Initialize PDF processor.
        
        Args:
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    
    def extract_documents_from_pdfs(self, uploaded_files: List) -> List[Document]:
        """
        Load PDFs and extract documents.
        
        Args:
            uploaded_files: List of uploaded PDF files
            
        Returns:
            List[Document]: Extracted LangChain documents
        """
        all_docs = []
        
        for pdf_file in uploaded_files:
            try:
                temp_path = save_uploaded_file(pdf_file, pdf_file.name)
                
                loader = PyPDFLoader(temp_path)
                docs = loader.load()
                
                all_docs.extend(docs)
                
            except Exception as e:
                logger.error(f"Error processing {pdf_file.name}: {str(e)}")
                raise
        
        logger.info(f"Extracted {len(all_docs)} pages from {len(uploaded_files)} PDF(s)")
        return all_docs
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks.
        
        Args:
            documents: List of documents to chunk
            
        Returns:
            List[Document]: Chunked documents
        """
        try:
            chunks = self.text_splitter.split_documents(documents)
            logger.info(f"Created {len(chunks)} text chunks")
            return chunks
        except Exception as e:
            logger.error(f"Error chunking documents: {str(e)}")
            raise
    
    def process_pdfs(self, uploaded_files: List) -> List[Document]:
        """
        Complete PDF processing pipeline.
        
        Args:
            uploaded_files: List of uploaded PDF files
            
        Returns:
            List[Document]: Processed and chunked documents
        """
        documents = self.extract_documents_from_pdfs(uploaded_files)
        chunks = self.chunk_documents(documents)
        return chunks
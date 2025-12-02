"""
PDF Chat RAG Application - Main Streamlit App
"""
import streamlit as st

from config.settings import settings
from src.utils.logger import logger
from src.services.pdf_processor import PDFProcessor
from src.services.vectorstore import VectorStoreService
from src.services.rag_chain import RAGChain
from src.ui.templates import CSS
from src.ui.components import (
    render_chat_history,
    render_sidebar_upload,
    render_process_button,
    render_clear_button
)


def initialize_session_state() -> None:
    """Initialize Streamlit session state variables."""
    if "rag_chain" not in st.session_state:
        st.session_state.rag_chain = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "processed" not in st.session_state:
        st.session_state.processed = False


def process_pdfs(uploaded_files) -> None:
    """
    Process uploaded PDFs and create RAG chain.
    
    Args:
        uploaded_files: List of uploaded PDF files
    """
    try:
        with st.spinner("Processing PDFs & building vector store..."):
            pdf_processor = PDFProcessor()
            chunks = pdf_processor.process_pdfs(uploaded_files)
            
            vectorstore_service = VectorStoreService()
            vectorstore = vectorstore_service.create_vectorstore(chunks)
            retriever = vectorstore_service.get_retriever(vectorstore)
            
            st.session_state.rag_chain = RAGChain(retriever)
            st.session_state.processed = True
            
        st.success("🎉 PDFs processed successfully! You can now ask questions.")
        
    except Exception as e:
        st.error(f"❌ Error processing PDFs: {str(e)}")
        logger.error(f"PDF processing failed: {str(e)}")


def handle_user_question(question: str) -> None:
    """
    Handle user question and display response.
    
    Args:
        question: User's question
    """
    if not st.session_state.rag_chain:
        st.warning("⚠️ Please upload and process PDFs first!")
        return
    
    # Check if this is a duplicate request
    if (st.session_state.get('last_question') == question and 
            st.session_state.get('last_response')):
        logger.info(f"Using cached response for: '{question[:50]}...'")
        return st.session_state.last_response
    
    try:
        with st.spinner("🤔 Thinking..."):
            answer, history = st.session_state.rag_chain.ask(question)
            st.session_state.chat_history = history
            # Store the last question and response to prevent duplicates
            st.session_state.last_question = question
            st.session_state.last_response = (answer, history)
            return answer, history
        
    except Exception as e:
        st.error(f"❌ Error generating response: {str(e)}")
        logger.error(f"Response generation failed: {str(e)}")
        return None, []


def main():
    """Main application function."""
    
    try:
        settings.validate()
    except ValueError as e:
        st.error(f"❌ Configuration Error: {str(e)}")
        st.info("💡 Please set GROQ_API_KEY in your .env file")
        st.stop()
    
    st.set_page_config(
        page_title=settings.PAGE_TITLE,
        page_icon=settings.PAGE_ICON,
        layout="wide"
    )
    
    st.write(CSS, unsafe_allow_html=True)
    
    initialize_session_state()
    
    st.header("Chat with Multiple PDFs — Powered by Groq LLM 🚀")
    st.markdown("---")
    
    uploaded_files = render_sidebar_upload()
    
    if render_process_button():
        if not uploaded_files:
            st.warning("⚠️ Please upload at least one PDF file!")
        else:
            process_pdfs(uploaded_files)
    
    if render_clear_button():
        if st.session_state.rag_chain:
            st.session_state.rag_chain.clear_memory()
            st.session_state.chat_history = []
            st.success("✅ Chat history cleared!")
            st.rerun()
    
    if st.session_state.processed:
        st.sidebar.success("✅ PDFs Ready for Questions")
    
    if st.session_state.chat_history:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        render_chat_history(st.session_state.chat_history)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("👋 Upload PDFs and start asking questions to begin the conversation!")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("---")
    col1, col2 = st.columns([6, 1])
    
    with col1:
        user_question = st.text_input(
            "💭 Ask a question about your documents:",
            placeholder="Type your question here...",
            key="user_input",
            label_visibility="collapsed"
        )
    
    with col2:
        ask_button = st.button("Send 📤", use_container_width=True, type="primary")
    
    if (ask_button or user_question) and user_question:
        handle_user_question(user_question)


if __name__ == "__main__":
    main()
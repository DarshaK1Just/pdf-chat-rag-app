"""
Reusable UI components for the Streamlit application.
"""
import streamlit as st
from typing import List
from langchain.schema import BaseMessage

from src.ui.templates import USER_TEMPLATE, BOT_TEMPLATE


def render_message(message: BaseMessage, index: int) -> None:
    """
    Render a single chat message.
    
    Args:
        message: Message to render
        index: Message index in history
    """
    is_user = index % 2 == 0
    template = USER_TEMPLATE if is_user else BOT_TEMPLATE
    
    st.write(
        template.replace("{{MSG}}", message.content),
        unsafe_allow_html=True
    )


def render_chat_history(history: List[BaseMessage]) -> None:
    """
    Render complete chat history.
    
    Args:
        history: List of chat messages
    """
    for i, message in enumerate(history):
        render_message(message, i)


def render_sidebar_upload() -> List:
    """
    Render PDF upload section in sidebar.
    
    Returns:
        List: Uploaded files
    """
    with st.sidebar:
        st.subheader("Upload Your PDF Documents")
        
        uploaded_files = st.file_uploader(
            "Upload PDFs",
            type=["pdf"],
            accept_multiple_files=True,
            help="Select one or more PDF files to chat with"
        )
        
        if uploaded_files:
            st.info(f"{len(uploaded_files)} file(s) uploaded")
        
        return uploaded_files


def render_process_button() -> bool:
    """
    Render process button in sidebar.
    
    Returns:
        bool: True if button clicked
    """
    with st.sidebar:
        return st.button(
            "Process PDFs",
            type="primary",
            use_container_width=True
        )


def render_clear_button() -> bool:
    """
    Render clear chat button in sidebar.
    
    Returns:
        bool: True if button clicked
    """
    with st.sidebar:
        st.divider()
        return st.button(
            "Clear Chat History",
            use_container_width=True
        )
# PDF Chat RAG Application

A Retrieval-Augmented Generation (RAG) application that allows users to chat with their PDF documents using Groq LLM and LangChain.

## Features

- Upload and process multiple PDF documents
- Interactive chat interface with conversation history
- Powered by Groq's Llama 3.3 70B model
- Semantic search using FAISS vector store
- Conversation memory for context-aware responses
- Clean and intuitive UI

## Project Structure

```
pdf-chat-rag/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Project dependencies
├── .env.example                    # Example environment variables
├── config/
│   └── settings.py                 # Configuration settings
├── src/
│   ├── utils/
│   │   ├── logger.py              # Logging configuration
│   │   └── file_handler.py        # File operations
│   ├── services/
│   │   ├── pdf_processor.py       # PDF processing logic
│   │   ├── vectorstore.py         # Vector store operations
│   │   └── rag_chain.py           # RAG chain implementation
│   └── ui/
│       ├── templates.py            # HTML/CSS templates
│       └── components.py           # Reusable UI components
└── tests/
    └── test_pdf_processor.py       # Unit tests
```

## Getting Started

### Prerequisites

- Python 3.8+
- Groq API key ([Get one here](https://console.groq.com))

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd pdf-chat-rag
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your GROQ_API_KEY
   ```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## Usage

1. **Upload PDFs**: Click on the sidebar and upload one or more PDF documents
2. **Process**: Click the "Process PDFs" button to index your documents
3. **Ask Questions**: Type your questions in the input field
4. **Chat**: View responses and maintain conversation context
5. **Clear History**: Use the "Clear Chat History" button to start fresh

## Configuration

Edit `config/settings.py` or use environment variables to customize:

- `LLM_MODEL`: Groq model to use (default: llama-3.3-70b-versatile)
- `LLM_TEMPERATURE`: Response randomness (default: 0.2)
- `CHUNK_SIZE`: Text chunk size (default: 1000)
- `CHUNK_OVERLAP`: Chunk overlap (default: 200)
- `EMBEDDING_MODEL`: Embedding model (default: sentence-transformers/all-MiniLM-L6-v2)

## Technology Stack

- **Frontend**: Streamlit
- **LLM**: Groq (Llama 3.3 70B)
- **Framework**: LangChain
- **Embeddings**: HuggingFace (sentence-transformers)
- **Vector Store**: FAISS
- **PDF Processing**: PyPDF2

## Best Practices Implemented

Modular architecture with separation of concerns  
Centralized configuration management  
Comprehensive logging  
Type hints for better code clarity  
Error handling and validation  
Reusable components  
Clean code structure  
Detailed documentation  
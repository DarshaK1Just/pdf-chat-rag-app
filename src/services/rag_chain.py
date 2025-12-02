"""
RAG chain service for question answering — fully updated for the new LangChain API.
"""
from typing import Tuple, List, Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

from config.settings import settings
from src.utils.logger import logger


# ---------------------------------------------------------
# Memory Store (Custom — Required by new LangChain API)
# ---------------------------------------------------------
class InMemoryChatHistory:
    """Simple chat history store compatible with RunnableWithMessageHistory."""

    def __init__(self):
        self.messages: List[BaseMessage] = []

    # Required by RunnableWithMessageHistory
    def add_messages(self, messages: List[BaseMessage]):
        """Add a list of messages (user or AI) to the history."""
        self.messages.extend(messages)

    def get_messages(self) -> List[BaseMessage]:
        return self.messages

    def clear(self):
        self.messages = []



# ---------------------------------------------------------
# RAGChain Implementation
# ---------------------------------------------------------
class RAGChain:
    """Retrieval-Augmented Generation chain using the modern LangChain architecture."""

    PROMPT_TEMPLATE = """
You are an expert document analyst providing precise, clear, and well-structured answers from PDF documents.

CORE PRINCIPLES:
1. Extract ONLY relevant information that answers the question
2. Use clear organization — bullets, headings, logical structure
3. Avoid redundancy and vague language
4. No filler phrases like "the document says" or "according to context"
5. If information is missing: say "This information is not available in the document"

CHAT HISTORY:
{chat_history}

QUESTION:
{question}

DOCUMENT CONTEXT:
{context}

YOUR ANSWER:
"""

    def __init__(
        self,
        retriever,
        model_name: str = settings.LLM_MODEL,
        temperature: float = settings.LLM_TEMPERATURE,
    ):
        """
        Args:
            retriever: Vector retriever instance
            model_name: Groq model (e.g., "mixtral-8x7b")
            temperature: LLM creativity level
        """
        self.retriever = retriever

        # NEW: Use ChatOpenAI with Groq's API endpoint
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=settings.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1",
        )

        # Build prompt template
        self.prompt = ChatPromptTemplate.from_template(self.PROMPT_TEMPLATE)

        # Chat history store (keyed by session_id)
        self.history_store: Dict[str, InMemoryChatHistory] = {
            "default": InMemoryChatHistory()
        }

        # Runnable chain with message history
        self.chain = RunnableWithMessageHistory(
            self._base_chain(),
            self._get_chat_history,
            input_messages_key="question",
            history_messages_key="chat_history",
        )

        logger.info(f"✓ RAG chain initialized using model: {model_name}")

    # ---------------------------------------------------------
    # Runnable chain logic
    # ---------------------------------------------------------
    def _base_chain(self):
        """LLM chain pipeline structure."""
        return self.prompt | self.llm

    def _get_chat_history(self, session_id: str):
        """Get chat history for the active session."""
        return self.history_store[session_id]

    # ---------------------------------------------------------
    # Helper for formatting memory
    # ---------------------------------------------------------
    def _format_chat_history(self, messages: List[BaseMessage]) -> str:
        if not messages:
            return "No previous conversation"

        formatted = []
        for msg in messages:
            role = "User" if isinstance(msg, HumanMessage) else "Assistant"
            formatted.append(f"{role}: {msg.content}")

        return "\n".join(formatted)

    # ---------------------------------------------------------
    # Main ask() method
    # ---------------------------------------------------------
    def ask(self, question: str) -> Tuple[str, List[BaseMessage]]:
        """Generate an answer using RAG with memory."""

        try:
            # Pull relevant chunks from FAISS or other retriever
            docs = self.retriever.invoke(question)
            context = "\n\n".join([d.page_content for d in docs])

            # Run the chain
            response = self.chain.invoke(
                {
                    "question": question,
                    "context": context,
                    "chat_history": "",  # Populated automatically
                },
                config={"session_id": "default"},
            )

            answer = response.content

            # Update memory manually
            history = self.history_store["default"]
            history.add_messages([
                HumanMessage(content=question),
                AIMessage(content=answer)
            ])

            logger.info(f"✓ RAG answer generated for: {question[:50]}...")

            return answer, history.get_messages()

        except Exception as e:
            logger.error(f"❌ RAGChain error: {str(e)}")
            raise

    # ---------------------------------------------------------
    # Memory clearing
    # ---------------------------------------------------------
    def clear_memory(self):
        """Reset conversation memory."""
        self.history_store["default"].clear()
        logger.info("✓ Chat history cleared")

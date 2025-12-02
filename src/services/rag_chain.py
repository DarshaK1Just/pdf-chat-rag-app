"""
RAG chain service for question answering.
"""
from typing import Tuple, List
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain.schema import BaseMessage

from config.settings import settings
from src.utils.logger import logger


class RAGChain:
    """Retrieval-Augmented Generation chain for question answering."""
    
    PROMPT_TEMPLATE = """You are an expert document analyst providing clear, accurate, and well-organized answers from PDF documents.

CORE PRINCIPLES:
1. Extract and present ONLY relevant information that directly answers the question
2. Organize information logically with clear structure
3. Be comprehensive but eliminate redundancy and unnecessary repetition
4. Use formatting strategically (bullets, numbered lists) for clarity
5. Focus on substance over form - avoid meta-commentary about the document itself

CHAT HISTORY:
{chat_history}

USER QUESTION:
{question}

DOCUMENT CONTEXT:
{context}

ANSWER REQUIREMENTS:
✓ Answer directly based on the context above
✓ Structure complex information with clear headings and bullets
✓ Present facts, data, and key points without repetition
✓ For summaries: focus on main ideas and essential details only
✓ For specific questions: provide precise answers with relevant context
✓ Avoid phrases like "the document mentions" or "according to the context"
✓ Don't repeat the same information in different sections
✓ If information is missing, state: "This information is not available in the document"

YOUR ANSWER:"""
    
    def __init__(
        self,
        retriever,
        model_name: str = settings.LLM_MODEL,
        temperature: float = settings.LLM_TEMPERATURE
    ):
        """
        Initialize RAG chain.
        
        Args:
            retriever: Document retriever
            model_name: LLM model name
            temperature: LLM temperature
        """
        self.retriever = retriever
        self.llm = ChatGroq(
            model_name=model_name,
            temperature=temperature,
            groq_api_key=settings.GROQ_API_KEY
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.prompt = ChatPromptTemplate.from_template(self.PROMPT_TEMPLATE)
        
        logger.info(f"✓ RAG chain ready with model: {model_name}")
    
    def _format_chat_history(self, messages: List[BaseMessage]) -> str:
        """
        Format chat history for prompt.
        
        Args:
            messages: List of chat messages
            
        Returns:
            str: Formatted chat history
        """
        if not messages:
            return "No previous conversation"
        
        formatted = []
        for msg in messages:
            role = "User" if msg.type == "human" else "Assistant"
            formatted.append(f"{role}: {msg.content}")
        return "\n".join(formatted)
    
    def ask(self, question: str) -> Tuple[str, List[BaseMessage]]:
        """
        Ask a question and get response.
        
        Args:
            question: User question
            
        Returns:
            Tuple[str, List[BaseMessage]]: Answer and chat history
        """
        try:
            # Retrieve relevant documents
            docs = self.retriever.get_relevant_documents(question)
            context = "\n\n".join([d.page_content for d in docs])
            
            # Get chat history
            chat_history = self.memory.load_memory_variables({})["chat_history"]
            formatted_history = self._format_chat_history(chat_history)
            
            # Format prompt
            final_prompt = self.prompt.format(
                question=question,
                context=context,
                chat_history=formatted_history
            )
            
            # Get response
            response = self.llm.invoke(final_prompt)
            
            # Save to memory
            self.memory.save_context(
                {"input": question},
                {"output": response.content}
            )
            
            logger.info(f"✓ Response generated for: '{question[:50]}...'")
            
            # Return response and updated history
            updated_history = self.memory.load_memory_variables({})["chat_history"]
            return response.content, updated_history
            
        except Exception as e:
            logger.error(f"Error in RAG chain: {str(e)}")
            raise
    
    def clear_memory(self) -> None:
        """Clear conversation memory."""
        self.memory.clear()
        logger.info("✓ Chat history cleared")
"""
LangChain RAG chat engine with conversation memory
"""
from typing import List, Dict, Optional, Tuple
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
import logging
import uuid
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ITHelpdeskChatEngine:
    """Chat engine for IT helpdesk with RAG and conversation memory"""
    
    def __init__(
        self,
        vector_store: Chroma,
        model_name: str = "gpt-4o-mini",
        temperature: float = 0.7,
        max_tokens: int = 500
    ):
        self.vector_store = vector_store
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        # Store conversation memories by conversation_id
        self.conversations: Dict[str, ConversationBufferMemory] = {}
        
        # Custom prompt template
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create custom prompt template for IT helpdesk"""
        template = """You are an expert IT helpdesk assistant for a company. Your role is to help employees with technical issues in a friendly, professional, and efficient manner.

Context from knowledge base:
{context}

Conversation history:
{chat_history}

User question: {question}

Instructions:
1. Provide clear, step-by-step solutions based on the knowledge base context
2. Be concise but thorough - employees need quick answers
3. Use numbered lists for multi-step instructions
4. If the solution involves multiple options, present them clearly
5. Be empathetic and professional
6. If you're unsure or the issue is complex, suggest contacting IT support
7. Include relevant troubleshooting steps
8. Use simple, non-technical language when possible
9. If the knowledge base doesn't contain the answer, be honest and suggest escalation

Your response:"""
        
        return PromptTemplate(
            template=template,
            input_variables=["context", "chat_history", "question"]
        )
    
    def _get_or_create_memory(self, conversation_id: str) -> ConversationBufferMemory:
        """Get existing conversation memory or create new one"""
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                output_key="answer"
            )
        
        return self.conversations[conversation_id]
    
    def _should_escalate(self, user_query: str, response: str) -> bool:
        """Determine if query should be escalated to human support"""
        escalation_keywords = [
            "don't know",
            "not sure",
            "unable to help",
            "contact it support",
            "call it",
            "submit a ticket",
            "hardware failure",
            "critical issue",
            "security breach",
            "emergency"
        ]
        
        response_lower = response.lower()
        query_lower = user_query.lower()
        
        # Check for escalation indicators
        for keyword in escalation_keywords:
            if keyword in response_lower or keyword in query_lower:
                return True
        
        # Check for urgency indicators
        urgency_keywords = ["urgent", "critical", "emergency", "immediately", "asap"]
        for keyword in urgency_keywords:
            if keyword in query_lower:
                return True
        
        return False
    
    def _extract_sources(self, source_documents: List) -> List[str]:
        """Extract and format source information"""
        sources = []
        seen = set()
        
        for doc in source_documents:
            source = doc.metadata.get("source", "IT Knowledge Base")
            category = doc.metadata.get("category", "")
            
            source_str = f"{source} - {category.title()}" if category else source
            
            if source_str not in seen:
                sources.append(source_str)
                seen.add(source_str)
        
        return sources[:3]  # Return top 3 unique sources
    
    def _generate_suggested_actions(self, response: str, category: str) -> List[str]:
        """Generate suggested follow-up actions based on response"""
        actions = []
        
        # Category-based suggestions
        category_actions = {
            "password": ["Check password requirements", "Contact IT if issue persists"],
            "networking": ["Test connection speed", "Try different network"],
            "audio_video": ["Check device settings", "Update drivers"],
            "hardware": ["Submit hardware request", "Check warranty status"],
            "software": ["Check software catalog", "Request IT approval"],
        }
        
        if category in category_actions:
            actions.extend(category_actions[category])
        
        # Response-based suggestions
        if "restart" in response.lower():
            actions.append("Restart your device")
        
        if "update" in response.lower():
            actions.append("Check for updates")
        
        if "contact" in response.lower() or "call" in response.lower():
            actions.append("Contact IT Support at x5555")
        
        return actions[:4]  # Return top 4 suggestions
    
    def chat(
        self,
        user_message: str,
        conversation_id: Optional[str] = None,
        user_context: Optional[Dict] = None
    ) -> Tuple[str, str, List[str], bool, List[str]]:
        """
        Process user message and return response
        
        Returns:
            Tuple of (response, conversation_id, sources, should_escalate, suggested_actions)
        """
        # Generate conversation ID if not provided
        if conversation_id is None:
            conversation_id = str(uuid.uuid4())
        
        logger.info(f"Processing message for conversation {conversation_id}")
        
        # Get or create conversation memory
        memory = self._get_or_create_memory(conversation_id)
        
        # Add user context to query if provided
        enhanced_query = user_message
        if user_context:
            context_str = " ".join([f"{k}: {v}" for k, v in user_context.items()])
            enhanced_query = f"{user_message}\n\nUser context: {context_str}"
        
        # Create retrieval chain
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 3}),
            memory=memory,
            return_source_documents=True,
            verbose=False
        )
        
        # Get response
        result = qa_chain({"question": enhanced_query})
        
        response = result["answer"]
        source_documents = result.get("source_documents", [])
        
        # Extract sources
        sources = self._extract_sources(source_documents)
        
        # Determine if escalation needed
        should_escalate = self._should_escalate(user_message, response)
        
        # Get category from top source
        category = "general"
        if source_documents:
            category = source_documents[0].metadata.get("category", "general")
        
        # Generate suggested actions
        suggested_actions = self._generate_suggested_actions(response, category)
        
        logger.info(f"Response generated (escalate: {should_escalate})")
        
        return response, conversation_id, sources, should_escalate, suggested_actions
    
    def clear_conversation(self, conversation_id: str) -> bool:
        """Clear conversation memory"""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            logger.info(f"Cleared conversation {conversation_id}")
            return True
        return False
    
    def get_conversation_history(self, conversation_id: str) -> List[Dict]:
        """Get conversation history"""
        if conversation_id not in self.conversations:
            return []
        
        memory = self.conversations[conversation_id]
        messages = memory.chat_memory.messages
        
        history = []
        for msg in messages:
            history.append({
                "role": "user" if msg.type == "human" else "assistant",
                "content": msg.content
            })
        
        return history


# Quick action message mapping
QUICK_ACTION_MESSAGES = {
    "reset_password": "How do I reset my password?",
    "wifi_help": "I'm having trouble connecting to Wi-Fi",
    "zoom_audio": "My Zoom audio isn't working",
    "printer_help": "I can't find or connect to the printer",
    "vpn_setup": "How do I set up VPN?",
    "slow_computer": "My computer is running very slow",
    "software_install": "How do I install new software?",
    "contact_support": "How can I contact IT support?"
}


def get_quick_action_message(action_id: str) -> Optional[str]:
    """Get predefined message for quick action"""
    return QUICK_ACTION_MESSAGES.get(action_id)


if __name__ == "__main__":
    # Test chat engine
    from knowledge_base import KnowledgeBaseLoader
    
    # Initialize knowledge base
    loader = KnowledgeBaseLoader()
    vector_store = loader.initialize()
    
    # Initialize chat engine
    chat_engine = ITHelpdeskChatEngine(vector_store)
    
    # Test conversation
    test_queries = [
        "How do I connect to the company Wi-Fi?",
        "What's the password?",
        "My Zoom audio isn't working"
    ]
    
    conv_id = None
    for query in test_queries:
        print(f"\nUser: {query}")
        response, conv_id, sources, escalate, actions = chat_engine.chat(query, conv_id)
        print(f"Assistant: {response}")
        print(f"Sources: {sources}")
        print(f"Escalate: {escalate}")
        print(f"Suggested actions: {actions}")


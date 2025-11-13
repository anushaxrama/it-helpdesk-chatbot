"""
FastAPI backend for IT Helpdesk Chatbot
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
import logging
from datetime import datetime
from typing import Dict
import uuid

from dotenv import load_dotenv

from models import (
    ChatRequest, ChatResponse, TicketRequest, TicketResponse,
    HealthResponse, QuickAction, AnalyticsEvent
)
from knowledge_base import KnowledgeBaseLoader, get_quick_actions
from chat_engine import ITHelpdeskChatEngine, get_quick_action_message

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global variables for chat engine and knowledge base
chat_engine: ITHelpdeskChatEngine = None
kb_loader: KnowledgeBaseLoader = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize services on startup"""
    global chat_engine, kb_loader
    
    logger.info("Starting IT Helpdesk Chatbot API...")
    
    # Verify OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        logger.error("OPENAI_API_KEY not set in environment variables!")
        raise ValueError("OPENAI_API_KEY must be set")
    
    # Initialize knowledge base
    logger.info("Initializing knowledge base...")
    kb_loader = KnowledgeBaseLoader(
        csv_path=os.getenv("KB_CSV_PATH", "data/it_knowledge.csv"),
        persist_directory=os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db"),
        collection_name=os.getenv("COLLECTION_NAME", "it_helpdesk")
    )
    vector_store = kb_loader.initialize()
    
    # Initialize chat engine
    logger.info("Initializing chat engine...")
    chat_engine = ITHelpdeskChatEngine(
        vector_store=vector_store,
        model_name=os.getenv("MODEL_NAME", "gpt-4o-mini"),
        temperature=float(os.getenv("TEMPERATURE", "0.7")),
        max_tokens=int(os.getenv("MAX_TOKENS", "500"))
    )
    
    logger.info("✅ IT Helpdesk Chatbot API started successfully!")
    
    yield
    
    # Cleanup
    logger.info("Shutting down IT Helpdesk Chatbot API...")


# Create FastAPI app
app = FastAPI(
    title="IT Helpdesk Chatbot API",
    description="AI-powered IT support chatbot using LangChain and OpenAI",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "message": "IT Helpdesk Chatbot API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0",
        components={
            "api": "healthy",
            "chat_engine": "healthy" if chat_engine else "unavailable",
            "knowledge_base": "healthy" if kb_loader else "unavailable",
            "vector_store": "healthy" if kb_loader and kb_loader.vector_store else "unavailable"
        }
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint for processing user queries
    """
    try:
        if not chat_engine:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Chat engine not initialized"
            )
        
        logger.info(f"Received chat request: {request.message[:50]}...")
        
        # Process message
        response, conv_id, sources, should_escalate, suggested_actions = chat_engine.chat(
            user_message=request.message,
            conversation_id=request.conversation_id,
            user_context=request.user_context
        )
        
        # Log analytics
        logger.info(f"Response generated for conversation {conv_id}")
        
        return ChatResponse(
            response=response,
            conversation_id=conv_id,
            sources=sources,
            suggested_actions=suggested_actions,
            should_escalate=should_escalate
        )
    
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat request: {str(e)}"
        )


@app.get("/quick-actions", response_model=list[QuickAction])
async def get_quick_action_buttons():
    """
    Get predefined quick action buttons
    """
    try:
        actions = get_quick_actions()
        return [QuickAction(**action) for action in actions]
    
    except Exception as e:
        logger.error(f"Error fetching quick actions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching quick actions"
        )


@app.post("/quick-action/{action_id}", response_model=ChatResponse)
async def process_quick_action(action_id: str, conversation_id: str = None):
    """
    Process a quick action button click
    """
    try:
        # Get predefined message for action
        message = get_quick_action_message(action_id)
        
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Quick action '{action_id}' not found"
            )
        
        # Process as regular chat message
        response, conv_id, sources, should_escalate, suggested_actions = chat_engine.chat(
            user_message=message,
            conversation_id=conversation_id
        )
        
        return ChatResponse(
            response=response,
            conversation_id=conv_id,
            sources=sources,
            suggested_actions=suggested_actions,
            should_escalate=should_escalate
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing quick action: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing quick action: {str(e)}"
        )


@app.post("/ticket", response_model=TicketResponse)
async def create_ticket(ticket: TicketRequest):
    """
    Create a support ticket for escalated issues
    """
    try:
        # In production, this would integrate with ServiceNow, Jira, etc.
        # For now, we'll simulate ticket creation
        
        ticket_id = f"TKT-{str(uuid.uuid4())[:8].upper()}"
        
        # Determine estimated response time based on priority
        response_times = {
            "low": "2-3 business days",
            "medium": "1 business day",
            "high": "4 hours",
            "critical": "1 hour"
        }
        
        estimated_time = response_times.get(ticket.priority.lower(), "1 business day")
        
        # Log ticket creation (in production, save to database)
        logger.info(f"Created ticket {ticket_id}: {ticket.issue_description[:50]}...")
        logger.info(f"Category: {ticket.category}, Priority: {ticket.priority}")
        
        return TicketResponse(
            ticket_id=ticket_id,
            status="created",
            estimated_response_time=estimated_time,
            message=f"Your support ticket {ticket_id} has been created. "
                   f"IT support will respond within {estimated_time}. "
                   f"You'll receive updates at {ticket.user_email or 'your email'}."
        )
    
    except Exception as e:
        logger.error(f"Error creating ticket: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating support ticket: {str(e)}"
        )


@app.delete("/conversation/{conversation_id}")
async def clear_conversation(conversation_id: str):
    """
    Clear conversation history
    """
    try:
        if not chat_engine:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Chat engine not initialized"
            )
        
        cleared = chat_engine.clear_conversation(conversation_id)
        
        if cleared:
            return {"message": f"Conversation {conversation_id} cleared successfully"}
        else:
            return {"message": f"Conversation {conversation_id} not found or already cleared"}
    
    except Exception as e:
        logger.error(f"Error clearing conversation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error clearing conversation: {str(e)}"
        )


@app.get("/conversation/{conversation_id}/history")
async def get_conversation_history(conversation_id: str):
    """
    Get conversation history
    """
    try:
        if not chat_engine:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Chat engine not initialized"
            )
        
        history = chat_engine.get_conversation_history(conversation_id)
        
        return {
            "conversation_id": conversation_id,
            "message_count": len(history),
            "messages": history
        }
    
    except Exception as e:
        logger.error(f"Error fetching conversation history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching conversation history: {str(e)}"
        )


@app.post("/analytics")
async def log_analytics(event: AnalyticsEvent):
    """
    Log analytics event (for tracking usage, satisfaction, etc.)
    """
    try:
        # In production, this would save to analytics database
        logger.info(f"Analytics event: {event.event_type}")
        logger.debug(f"Event details: {event.model_dump()}")
        
        return {"message": "Analytics event logged successfully"}
    
    except Exception as e:
        logger.error(f"Error logging analytics: {str(e)}")
        # Don't fail on analytics errors
        return {"message": "Analytics logging failed", "error": str(e)}


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "detail": str(exc)
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    )


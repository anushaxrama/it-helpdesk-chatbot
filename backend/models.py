"""
Pydantic models for request/response validation
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class ChatMessage(BaseModel):
    """Single chat message"""
    role: str = Field(..., description="Role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: Optional[str] = Field(None, description="ISO timestamp")


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str = Field(..., min_length=1, max_length=2000, description="User message")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context")
    user_context: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Additional context (OS, location, etc.)"
    )


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str = Field(..., description="Assistant response")
    conversation_id: str = Field(..., description="Conversation ID")
    sources: Optional[List[str]] = Field(default_factory=list, description="Knowledge base sources used")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Response confidence score")
    suggested_actions: Optional[List[str]] = Field(
        default_factory=list,
        description="Suggested follow-up actions"
    )
    should_escalate: bool = Field(False, description="Whether to escalate to human support")


class TicketRequest(BaseModel):
    """Request model for creating support ticket"""
    issue_description: str = Field(..., min_length=10, max_length=5000)
    category: str = Field(..., description="Issue category")
    priority: str = Field("medium", description="Priority: low, medium, high, critical")
    user_email: Optional[str] = Field(None, description="User email")
    user_name: Optional[str] = Field(None, description="User name")
    conversation_id: Optional[str] = Field(None, description="Related conversation ID")


class TicketResponse(BaseModel):
    """Response model for ticket creation"""
    ticket_id: str = Field(..., description="Generated ticket ID")
    status: str = Field("created", description="Ticket status")
    estimated_response_time: str = Field(..., description="Estimated response time")
    message: str = Field(..., description="Confirmation message")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    timestamp: str = Field(..., description="Current timestamp")
    version: str = Field(..., description="API version")
    components: Dict[str, str] = Field(
        default_factory=dict,
        description="Status of individual components"
    )


class QuickAction(BaseModel):
    """Quick action button definition"""
    id: str = Field(..., description="Action identifier")
    label: str = Field(..., description="Button label")
    description: str = Field(..., description="Action description")
    category: str = Field(..., description="Action category")
    icon: Optional[str] = Field(None, description="Icon name or emoji")


class AnalyticsEvent(BaseModel):
    """Analytics/logging event"""
    event_type: str = Field(..., description="Event type")
    conversation_id: Optional[str] = Field(None)
    user_query: Optional[str] = Field(None)
    response_time_ms: Optional[float] = Field(None)
    was_helpful: Optional[bool] = Field(None)
    category: Optional[str] = Field(None)
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


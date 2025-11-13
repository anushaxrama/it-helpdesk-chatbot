export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  sources?: string[];
  suggestedActions?: string[];
}

export interface ChatRequest {
  message: string;
  conversation_id?: string;
  user_context?: Record<string, any>;
}

export interface ChatResponse {
  response: string;
  conversation_id: string;
  sources?: string[];
  confidence?: number;
  suggested_actions?: string[];
  should_escalate: boolean;
}

export interface QuickAction {
  id: string;
  label: string;
  description: string;
  category: string;
  icon?: string;
}

export interface TicketRequest {
  issue_description: string;
  category: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
  user_email?: string;
  user_name?: string;
  conversation_id?: string;
}

export interface TicketResponse {
  ticket_id: string;
  status: string;
  estimated_response_time: string;
  message: string;
}


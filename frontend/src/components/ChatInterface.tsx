import React, { useState, useEffect, useRef } from 'react';
import { Send, RefreshCw, AlertCircle } from 'lucide-react';
import { MessageBubble } from './MessageBubble';
import { QuickActions } from './QuickActions';
import { TypingIndicator } from './TypingIndicator';
import { EscalationBanner } from './EscalationBanner';
import { chatApi } from '../api/chatApi';
import type { Message, QuickAction } from '../types';

export const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | undefined>();
  const [quickActions, setQuickActions] = useState<QuickAction[]>([]);
  const [showEscalation, setShowEscalation] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isConnected, setIsConnected] = useState(true);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Scroll to bottom when messages change
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  // Load quick actions on mount
  useEffect(() => {
    const loadQuickActions = async () => {
      try {
        const actions = await chatApi.getQuickActions();
        setQuickActions(actions);
      } catch (error) {
        console.error('Failed to load quick actions:', error);
      }
    };

    const checkConnection = async () => {
      try {
        await chatApi.checkHealth();
        setIsConnected(true);
      } catch (error) {
        console.error('Backend not connected:', error);
        setIsConnected(false);
        setError('Cannot connect to backend. Please ensure the server is running on http://localhost:8000');
      }
    };

    loadQuickActions();
    checkConnection();

    // Add welcome message
    setMessages([
      {
        id: '1',
        role: 'assistant',
        content: "👋 Hi! I'm your IT Helpdesk Assistant. I can help you with:\n\n• Password resets and account issues\n• Wi-Fi and VPN connectivity\n• Software installation and updates\n• Audio/video troubleshooting\n• Printer and hardware problems\n• And much more!\n\nHow can I help you today?",
        timestamp: new Date().toISOString(),
      },
    ]);
  }, []);

  const handleSendMessage = async (messageText?: string) => {
    const text = messageText || inputValue.trim();
    if (!text || isLoading) return;

    setError(null);
    
    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: text,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Send to API
      const response = await chatApi.sendMessage({
        message: text,
        conversation_id: conversationId,
      });

      // Update conversation ID
      if (!conversationId) {
        setConversationId(response.conversation_id);
      }

      // Add assistant response
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.response,
        timestamp: new Date().toISOString(),
        sources: response.sources,
        suggestedActions: response.suggested_actions,
      };

      setMessages((prev) => [...prev, assistantMessage]);

      // Show escalation banner if needed
      if (response.should_escalate) {
        setShowEscalation(true);
      }
    } catch (error: any) {
      console.error('Error sending message:', error);
      
      let errorMessage = 'Sorry, I encountered an error. Please try again.';
      if (error.response?.status === 503) {
        errorMessage = 'The chat service is temporarily unavailable. Please try again in a moment.';
      } else if (error.message?.includes('Network Error')) {
        errorMessage = 'Cannot connect to the server. Please check if the backend is running.';
        setIsConnected(false);
      }
      
      setError(errorMessage);
      
      const errorMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: errorMessage,
        timestamp: new Date().toISOString(),
      };
      
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleQuickAction = async (actionId: string) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await chatApi.processQuickAction(actionId, conversationId);

      if (!conversationId) {
        setConversationId(response.conversation_id);
      }

      // Get the quick action details for display
      const action = quickActions.find(a => a.id === actionId);
      
      // Add user message
      const userMessage: Message = {
        id: Date.now().toString(),
        role: 'user',
        content: action?.description || actionId,
        timestamp: new Date().toISOString(),
      };

      // Add assistant response
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.response,
        timestamp: new Date().toISOString(),
        sources: response.sources,
        suggestedActions: response.suggested_actions,
      };

      setMessages((prev) => [...prev, userMessage, assistantMessage]);

      if (response.should_escalate) {
        setShowEscalation(true);
      }
    } catch (error) {
      console.error('Error processing quick action:', error);
      setError('Failed to process quick action. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearChat = () => {
    if (window.confirm('Are you sure you want to clear this conversation?')) {
      setMessages([
        {
          id: '1',
          role: 'assistant',
          content: "Chat cleared. How can I help you today?",
          timestamp: new Date().toISOString(),
        },
      ]);
      setConversationId(undefined);
      setShowEscalation(false);
      setError(null);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4 shadow-sm">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-primary-600 rounded-xl flex items-center justify-center">
              <span className="text-white text-xl">🤖</span>
            </div>
            <div>
              <h1 className="text-lg font-bold text-gray-900">IT Helpdesk Assistant</h1>
              <p className="text-sm text-gray-500">
                {isConnected ? (
                  <>
                    <span className="inline-block w-2 h-2 bg-green-500 rounded-full mr-1.5"></span>
                    Online
                  </>
                ) : (
                  <>
                    <span className="inline-block w-2 h-2 bg-red-500 rounded-full mr-1.5"></span>
                    Offline
                  </>
                )}
              </p>
            </div>
          </div>
          <button
            onClick={handleClearChat}
            className="btn btn-secondary text-sm flex items-center gap-2"
            title="Clear conversation"
          >
            <RefreshCw className="w-4 h-4" />
            Clear Chat
          </button>
        </div>
      </div>

      {/* Connection Error Banner */}
      {!isConnected && (
        <div className="bg-red-50 border-b border-red-200 px-6 py-3">
          <div className="flex items-center gap-2 text-sm text-red-800">
            <AlertCircle className="w-4 h-4" />
            <span>Backend server is not running. Start it with: <code className="bg-red-100 px-2 py-0.5 rounded">cd backend && python main.py</code></span>
          </div>
        </div>
      )}

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto custom-scrollbar px-6 py-4">
        <div className="max-w-4xl mx-auto">
          {/* Escalation Banner */}
          {showEscalation && conversationId && (
            <EscalationBanner
              conversationId={conversationId}
              onClose={() => setShowEscalation(false)}
            />
          )}

          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
              <div className="flex items-start gap-2">
                <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                <p className="text-sm text-red-800">{error}</p>
              </div>
            </div>
          )}

          {/* Messages */}
          {messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}

          {/* Typing Indicator */}
          {isLoading && <TypingIndicator />}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Quick Actions */}
      {quickActions.length > 0 && messages.length <= 1 && (
        <QuickActions
          actions={quickActions}
          onActionClick={handleQuickAction}
          disabled={isLoading || !isConnected}
        />
      )}

      {/* Input Area */}
      <div className="bg-white border-t border-gray-200 px-6 py-4 shadow-lg">
        <div className="max-w-4xl mx-auto">
          <div className="flex gap-3">
            <input
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your IT question here..."
              disabled={isLoading || !isConnected}
              className="input flex-1 disabled:bg-gray-100"
            />
            <button
              onClick={() => handleSendMessage()}
              disabled={!inputValue.trim() || isLoading || !isConnected}
              className="btn btn-primary px-6 flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className="w-4 h-4" />
              Send
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-2 text-center">
            Press Enter to send • AI responses may not always be accurate
          </p>
        </div>
      </div>
    </div>
  );
};


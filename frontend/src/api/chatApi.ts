import axios, { AxiosInstance } from 'axios';
import type { ChatRequest, ChatResponse, QuickAction, TicketRequest, TicketResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

class ChatAPI {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    const response = await this.client.post<ChatResponse>('/chat', request);
    return response.data;
  }

  async getQuickActions(): Promise<QuickAction[]> {
    const response = await this.client.get<QuickAction[]>('/quick-actions');
    return response.data;
  }

  async processQuickAction(actionId: string, conversationId?: string): Promise<ChatResponse> {
    const params = conversationId ? { conversation_id: conversationId } : {};
    const response = await this.client.post<ChatResponse>(`/quick-action/${actionId}`, null, { params });
    return response.data;
  }

  async createTicket(request: TicketRequest): Promise<TicketResponse> {
    const response = await this.client.post<TicketResponse>('/ticket', request);
    return response.data;
  }

  async clearConversation(conversationId: string): Promise<void> {
    await this.client.delete(`/conversation/${conversationId}`);
  }

  async getConversationHistory(conversationId: string): Promise<any> {
    const response = await this.client.get(`/conversation/${conversationId}/history`);
    return response.data;
  }

  async checkHealth(): Promise<any> {
    const response = await this.client.get('/health');
    return response.data;
  }
}

export const chatApi = new ChatAPI();


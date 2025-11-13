import React, { useState } from 'react';
import { AlertCircle, X, Send } from 'lucide-react';
import { chatApi } from '../api/chatApi';
import type { TicketRequest } from '../types';

interface EscalationBannerProps {
  conversationId: string;
  onClose: () => void;
}

export const EscalationBanner: React.FC<EscalationBannerProps> = ({ 
  conversationId, 
  onClose 
}) => {
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [ticketId, setTicketId] = useState<string>('');
  
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    description: '',
    priority: 'medium' as 'low' | 'medium' | 'high' | 'critical',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const request: TicketRequest = {
        issue_description: formData.description,
        category: 'general',
        priority: formData.priority,
        user_name: formData.name,
        user_email: formData.email,
        conversation_id: conversationId,
      };

      const response = await chatApi.createTicket(request);
      setTicketId(response.ticket_id);
      setSuccess(true);
    } catch (error) {
      console.error('Error creating ticket:', error);
      alert('Failed to create ticket. Please try again or contact IT directly.');
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
        <div className="flex items-start gap-3">
          <div className="flex-shrink-0">
            <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
              <Send className="w-4 h-4 text-green-600" />
            </div>
          </div>
          <div className="flex-1">
            <h3 className="text-sm font-semibold text-green-900 mb-1">
              Ticket Created Successfully!
            </h3>
            <p className="text-sm text-green-800">
              Your support ticket <strong>{ticketId}</strong> has been created. 
              IT support will contact you soon.
            </p>
          </div>
          <button
            onClick={onClose}
            className="flex-shrink-0 text-green-600 hover:text-green-800"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
      </div>
    );
  }

  if (showForm) {
    return (
      <div className="bg-orange-50 border border-orange-200 rounded-lg p-4 mb-4">
        <div className="flex items-start gap-3 mb-4">
          <div className="flex-shrink-0">
            <div className="w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center">
              <AlertCircle className="w-4 h-4 text-orange-600" />
            </div>
          </div>
          <div className="flex-1">
            <h3 className="text-sm font-semibold text-orange-900 mb-1">
              Create Support Ticket
            </h3>
            <p className="text-sm text-orange-800 mb-3">
              Fill out the form below to escalate this issue to IT support.
            </p>
          </div>
          <button
            onClick={() => setShowForm(false)}
            className="flex-shrink-0 text-orange-600 hover:text-orange-800"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-3">
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">
              Your Name *
            </label>
            <input
              type="text"
              required
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className="input text-sm"
              placeholder="John Doe"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">
              Email Address *
            </label>
            <input
              type="email"
              required
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              className="input text-sm"
              placeholder="john.doe@company.com"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">
              Issue Description *
            </label>
            <textarea
              required
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              className="input text-sm min-h-[80px]"
              placeholder="Describe your issue in detail..."
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">
              Priority
            </label>
            <select
              value={formData.priority}
              onChange={(e) => setFormData({ ...formData, priority: e.target.value as any })}
              className="input text-sm"
            >
              <option value="low">Low - Can wait 2-3 days</option>
              <option value="medium">Medium - Need help within 1 day</option>
              <option value="high">High - Blocking my work</option>
              <option value="critical">Critical - System down</option>
            </select>
          </div>

          <div className="flex gap-2 pt-2">
            <button
              type="submit"
              disabled={loading}
              className="btn btn-primary text-sm flex-1"
            >
              {loading ? 'Creating...' : 'Create Ticket'}
            </button>
            <button
              type="button"
              onClick={() => setShowForm(false)}
              className="btn btn-secondary text-sm"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    );
  }

  return (
    <div className="bg-orange-50 border border-orange-200 rounded-lg p-4 mb-4">
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0">
          <div className="w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center">
            <AlertCircle className="w-4 h-4 text-orange-600" />
          </div>
        </div>
        <div className="flex-1">
          <h3 className="text-sm font-semibold text-orange-900 mb-1">
            Need More Help?
          </h3>
          <p className="text-sm text-orange-800 mb-3">
            This issue may require assistance from IT support. You can create a ticket or contact us directly.
          </p>
          <div className="flex gap-2">
            <button
              onClick={() => setShowForm(true)}
              className="text-xs font-medium text-orange-700 hover:text-orange-900 px-3 py-1.5 bg-white border border-orange-300 rounded-md hover:bg-orange-50"
            >
              Create Ticket
            </button>
            <a
              href="tel:x5555"
              className="text-xs font-medium text-orange-700 hover:text-orange-900 px-3 py-1.5 bg-white border border-orange-300 rounded-md hover:bg-orange-50"
            >
              Call x5555
            </a>
          </div>
        </div>
        <button
          onClick={onClose}
          className="flex-shrink-0 text-orange-600 hover:text-orange-800"
        >
          <X className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
};


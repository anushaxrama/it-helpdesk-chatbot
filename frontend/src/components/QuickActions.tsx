import React from 'react';
import type { QuickAction } from '../types';

interface QuickActionsProps {
  actions: QuickAction[];
  onActionClick: (actionId: string) => void;
  disabled?: boolean;
}

export const QuickActions: React.FC<QuickActionsProps> = ({ 
  actions, 
  onActionClick, 
  disabled = false 
}) => {
  return (
    <div className="bg-white border-t border-gray-200 p-4">
      <h3 className="text-sm font-semibold text-gray-700 mb-3">Quick Actions</h3>
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
        {actions.map((action) => (
          <button
            key={action.id}
            onClick={() => onActionClick(action.id)}
            disabled={disabled}
            className="flex flex-col items-center gap-2 p-3 bg-gray-50 hover:bg-primary-50 border border-gray-200 hover:border-primary-300 rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed group"
            title={action.description}
          >
            <span className="text-2xl group-hover:scale-110 transition-transform">
              {action.icon || '🔧'}
            </span>
            <span className="text-xs font-medium text-gray-700 group-hover:text-primary-700 text-center leading-tight">
              {action.label}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
};


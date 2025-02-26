import React from 'react';
import { Button } from 'react-bootstrap';

const ChatMessage = ({ message }) => {
  const handleSuggestionClick = (action) => {
    if (action.startsWith('http')) {
      window.open(action, '_blank');
    } else {
      console.log('Unhandled action:', action); // For future commands
    }
  };

  return (
    <div className={`d-flex justify-content-${message.sender === 'user' ? 'end' : 'start'} mb-3`}>
      <div
        className={`p-3 rounded-3 bg-${message.sender === 'user' ? 'primary' : 'secondary'} text-white`}
        style={{ maxWidth: '70%', wordBreak: 'break-word' }}
      >
        <div className="fw-bold">{message.sender.toUpperCase()}</div>
        {message.text}
        {message.metadata && (
          <div className="mt-2 text-white-50">
            <small>Analysis: {message.metadata.visualization || 'None'}</small>
          </div>
        )}
        {message.suggestions && message.suggestions.length > 0 && (
          <div className="mt-2">
            {message.suggestions.map((suggestion, i) => (
              <Button
                key={i}
                variant="outline-light"
                size="sm"
                className="me-2 mb-2"
                onClick={() => handleSuggestionClick(suggestion.action)}
              >
                {suggestion.label}
              </Button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatMessage;

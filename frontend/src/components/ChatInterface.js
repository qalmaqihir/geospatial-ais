import React, { useState, useEffect, useRef } from 'react';
import { Card, Form, Button, Dropdown, Spinner } from 'react-bootstrap';
import ChatMessage from './ChatMessage';

const ChatInterface = ({ messages, setMessages, isLoading, selectedModel, setSelectedModel, handleChatSubmit }) => {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    handleChatSubmit(input);
    setInput('');
  };

  return (
    <Card style={{ height: '85vh' }}>
      <Card.Header className="d-flex justify-content-between align-items-center">
        <Dropdown onSelect={(e) => setSelectedModel(e)}>
          <Dropdown.Toggle variant="primary" id="model-select">
            {selectedModel.toUpperCase()}
          </Dropdown.Toggle>
          <Dropdown.Menu>
            <Dropdown.Item eventKey="gpt-4">GPT-4</Dropdown.Item>
            <Dropdown.Item eventKey="gpt-3">GPT-3</Dropdown.Item>
            <Dropdown.Item eventKey="claude-2">Claude 2</Dropdown.Item>
            <Dropdown.Item eventKey="gemmni">Gemmni</Dropdown.Item>
            <Dropdown.Item eventKey="deepseek">Deepseek</Dropdown.Item>
            
          </Dropdown.Menu>
        </Dropdown>
        {isLoading && <Spinner animation="border" size="sm" />}
      </Card.Header>
      <Card.Body className="overflow-auto">
        {messages.map((msg, i) => (
          <ChatMessage key={i} message={msg} />
        ))}
        <div ref={messagesEndRef} />
      </Card.Body>
      <Card.Footer>
        <Form onSubmit={handleSubmit}>
          <Form.Group>
            <Form.Control
              as="textarea"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about the map (e.g., 'Show me New York', 'What's here?')"
              disabled={isLoading}
            />
            <div className="d-flex justify-content-between mt-2">
              <small className="text-muted">Press Enter to send</small>
              <Button type="submit" disabled={!input.trim() || isLoading}>
                {isLoading ? 'Sending...' : 'Send'}
              </Button>
            </div>
          </Form.Group>
        </Form>
      </Card.Footer>
    </Card>
  );
};

export default ChatInterface;
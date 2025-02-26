import React from 'react';
import { Spinner } from 'react-bootstrap';

const LoadingSpinner = () => (
  <Spinner animation="border" size="sm" role="status">
    <span className="visually-hidden">Loading...</span>
  </Spinner>
);

export default LoadingSpinner;
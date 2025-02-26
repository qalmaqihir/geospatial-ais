import React from 'react';
import { Form, Button, Dropdown, Alert } from 'react-bootstrap';
import { FaSearch, FaMapMarkedAlt } from 'react-icons/fa';

const LocationSearch = ({
  handleLocationSearch,
  handleUseCurrentLocation,
  mapStyle,
  setMapStyle,
  isLoading,
  error,
  setError,
  currentCoords,
  zoomLevel,
}) => {
  const mapStyles = [
    { name: 'OpenStreetMap', url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', attribution: '© OpenStreetMap contributors' },
    { name: 'Satellite', url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attribution: 'Tiles © Esri' },
    { name: 'Terrain', url: 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', attribution: 'OpenTopoMap' },
  ];

  return (
    <div className="search-bar">
      <Form onSubmit={handleLocationSearch} className="d-flex gap-2 align-items-center">
        <Form.Control
          name="location"
          placeholder="Enter location or coordinates (e.g., 'New York' or '40.7128, -74.0060')"
          disabled={isLoading}
        />
        <Button type="submit" className="btn-custom" variant="primary" disabled={isLoading}>
          <FaSearch /> {isLoading ? 'Searching...' : 'Search'}
        </Button>
        <Button variant="info" className="btn-custom" onClick={handleUseCurrentLocation} disabled={isLoading}>
          <FaMapMarkedAlt /> Current Location
        </Button>
        <Dropdown onSelect={(styleKey) => setMapStyle(mapStyles[styleKey])}>
          <Dropdown.Toggle variant="secondary" className="btn-custom">
            {mapStyle.name}
          </Dropdown.Toggle>
          <Dropdown.Menu>
            {mapStyles.map((style, i) => (
              <Dropdown.Item key={style.name} eventKey={i}>{style.name}</Dropdown.Item>
            ))}
          </Dropdown.Menu>
        </Dropdown>
      </Form>
      {error && (
        <Alert variant="danger" dismissible onClose={() => setError('')} className="mt-2">
          {error}
        </Alert>
      )}
      <small className="text-muted">
        Current view: {currentCoords[0].toFixed(4)}, {currentCoords[1].toFixed(4)} (Zoom: {zoomLevel})
      </small>
    </div>
  );
};

export default LocationSearch;
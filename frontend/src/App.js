import React, { useState, useEffect } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import MapContainer from './components/MapContainer';
import ChatInterface from './components/ChatInterface';
import LocationSearch from './components/LocationSearch';
import { startSession, sendChatMessage, geocodeLocation } from './services/apiService';
import { validateCoordinates } from './utils/geoUtils';
import { v4 as uuidv4 } from 'uuid';

const DEFAULT_COORDS = [51.505, -0.09];

const App = () => {
  const [messages, setMessages] = useState([]);
  const [location, setLocation] = useState(DEFAULT_COORDS);
  const [mapStyle, setMapStyle] = useState({
    name: 'OpenStreetMap',
    url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    attribution: '© OpenStreetMap contributors',
  });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentCoords, setCurrentCoords] = useState(DEFAULT_COORDS);
  const [zoomLevel, setZoomLevel] = useState(13);
  const [markers, setMarkers] = useState([]);
  const [selectedArea, setSelectedArea] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [selectedModel, setSelectedModel] = useState('gpt-4');
  const [visualization, setVisualization] = useState(null);
  useEffect(() => {
    const initializeSession = async () => {
      try {
        const session = await startSession();
        setSessionId(session);
      } catch (err) {
        setError(err.message);
      }
    };
    initializeSession();
  }, []);

  // const handleChatSubmit = async (message) => {
  //   setMessages((prev) => [...prev, { text: message, sender: 'user' }]);
  //   setIsLoading(true);
  //   try {
  //     const response = await sendChatMessage(message, selectedModel, sessionId, currentCoords, selectedArea);
  //     setMessages((prev) => [...prev, { text: response.text, sender: 'ai', metadata: response.analysis, suggestions: response.suggestions }]);
  //     setVisualization(response.analysis?.visualization || null); // Set visualization from AI
  //   } catch (err) {
  //     setError(err.message);
  //   } finally {
  //     setIsLoading(false);
  //   }
  // };
// ... (previous imports and state remain the same)
  const handleChatSubmit = async (message) => {
    setMessages((prev) => [...prev, { text: message, sender: 'user' }]);
    setIsLoading(true);
    try {
      const response = await sendChatMessage(message, selectedModel, sessionId, {
        coordinates: currentCoords,
        zoomLevel: zoomLevel,
        selectedArea: selectedArea
      }, selectedArea);
      setMessages((prev) => [...prev, { text: response.text, sender: 'ai', metadata: response.metadata, suggestions: response.suggestions }]);
      setVisualization(response.metadata?.visualization || null);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };
// ... (rest of the component remains the same)

  const handleMapClick = (e) => {
    const newMarker = { id: uuidv4(), lat: e.latlng.lat, lng: e.latlng.lng, timestamp: new Date().toISOString() };
    setMarkers([...markers, newMarker]);
  };

  const handleMapMove = (coords, zoom) => {
    setCurrentCoords(coords);
    setZoomLevel(zoom);
  };

  const handleLocationSearch = async (e) => {
    e.preventDefault();
    const input = e.target.elements.location.value.trim();
    if (!input) return;

    setError('');
    setIsLoading(true);

    try {
      let coords = [];
      if (validateCoordinates(input)) {
        coords = input.split(/[,\s]+/).map(Number);
        if (Math.abs(coords[0]) > 90 || Math.abs(coords[1]) > 180) {
          throw new Error('Invalid coordinates. Latitude: -90 to 90, Longitude: -180 to 180');
        }
        setLocation(coords);
      } else {
        const { lat, lon } = await geocodeLocation(input);
        setLocation([lat, lon]);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleUseCurrentLocation = () => {
    if (!navigator.geolocation) {
      setError('Geolocation not supported by your browser');
      return;
    }
    setIsLoading(true);
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setLocation([position.coords.latitude, position.coords.longitude]);
        setIsLoading(false);
      },
      (err) => {
        setError(`Unable to retrieve location: ${err.message}`);
        setIsLoading(false);
      }
    );
  };

  return (
    <Container fluid>
      <Row className="mb-2">
        <Col>
          <LocationSearch
            handleLocationSearch={handleLocationSearch}
            handleUseCurrentLocation={handleUseCurrentLocation}
            mapStyle={mapStyle}
            setMapStyle={setMapStyle}
            isLoading={isLoading}
            error={error}
            setError={setError}
            currentCoords={currentCoords}
            zoomLevel={zoomLevel}
          />
        </Col>
      </Row>
      <Row>
        <Col md={6}>
          <ChatInterface
            messages={messages}
            setMessages={setMessages}
            isLoading={isLoading}
            selectedModel={selectedModel}
            setSelectedModel={setSelectedModel}
            handleChatSubmit={handleChatSubmit}
          />
        </Col>
        <Col md={6}>
          <MapContainer
            location={location}
            mapStyle={mapStyle}
            markers={markers}
            setMarkers={setMarkers}
            selectedArea={selectedArea}
            setSelectedArea={setSelectedArea}
            onMapMove={handleMapMove}
            onMapClick={handleMapClick}
            visualization={visualization}
          />
        </Col>
      </Row>
    </Container>
  );
};

export default App;


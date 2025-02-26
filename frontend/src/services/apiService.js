// import axios from 'axios';

// const api = axios.create({
//   baseURL: 'http://localhost:5000',  // Remove '/api' from baseURL
//   headers: { 'Content-Type': 'application/json' },
//   withCredentials: true,  // Ensure cookies are sent
// });

// export const startSession = async () => {
//   try {
//     const response = await api.post('/api/session');  // Explicitly include /api
//     const sessionCookie = response.headers['set-cookie']?.[0] || null;
//     return sessionCookie ? sessionCookie.split(';')[0] : 'default-session';
//   } catch (error) {
//     throw new Error(`Failed to start session: ${error.message}`);
//   }
// };

// export const sendChatMessage = async (message, model, sessionId, coordinates, selectedArea) => {
//   try {
//     const response = await api.post('/api/chat', {
//       message,
//       model,
//       session: sessionId,
//       coordinates: { coordinates, zoom: coordinates.zoomLevel, selectedArea },
//     });
//     return response.data;
//   } catch (error) {
//     throw new Error(`Chat request failed: ${error.message}`);
//   }
// };

// export const geocodeLocation = async (location) => {
//   try {
//     const response = await api.get(`/api/geocode?location=${encodeURIComponent(location)}`);
//     if (response.data.error) throw new Error(response.data.error);
//     return { lat: response.data.lat, lon: response.data.lon };
//   } catch (error) {
//     throw new Error(`Geocoding failed: ${error.message}`);
//   }
// };


import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000',
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true,
});

export const startSession = async () => {
  try {
    const response = await api.post('/api/session');
    const sessionCookie = response.headers['set-cookie']?.[0] || null;
    return sessionCookie ? sessionCookie.split(';')[0] : 'default-session';
  } catch (error) {
    throw new Error(`Failed to start session: ${error.message}`);
  }
};

export const sendChatMessage = async (message, model, sessionId, coordinates, selectedArea) => {
  try {
    // Fix coordinates object structure
    const payload = {
      message,
      model,
      session: sessionId,
      coordinates: {
        coordinates: coordinates,  // Array [lat, lng]
        zoom: coordinates?.zoomLevel || 13,  // Use zoomLevel from App.js
        selectedArea: selectedArea || null
      }
    };
    console.log('Sending chat payload:', payload);  // Debug log
    const response = await api.post('/api/chat', payload);
    return response.data;
  } catch (error) {
    console.error('Chat error:', error);  // Debug log
    throw new Error(`Chat request failed: ${error.message}`);
  }
};

export const geocodeLocation = async (location) => {
  try {
    const response = await api.get(`/api/geocode?location=${encodeURIComponent(location)}`);
    if (response.data.error) throw new Error(response.data.error);
    return { lat: response.data.lat, lon: response.data.lon };
  } catch (error) {
    throw new Error(`Geocoding failed: ${error.message}`);
  }
};
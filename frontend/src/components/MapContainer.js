// import React, { useEffect, useState } from 'react';
// import { MapContainer as LeafletMap, Marker, Popup, Rectangle, useMap } from 'react-leaflet';
// import MapView from './MapView';
// import 'leaflet/dist/leaflet.css';
// import 'leaflet-draw/dist/leaflet.draw.css';
// import L from 'leaflet';
// import 'leaflet-draw';
// import 'leaflet.heat';

// const MapContainerComponent = ({ location, mapStyle, markers, setMarkers, selectedArea, setSelectedArea, onMapMove, onMapClick, visualization }) => {
//   const map = useMap();
//   const [heatmapLayer, setHeatmapLayer] = useState(null);

//   useEffect(() => {
//     const drawnItems = new L.FeatureGroup();
//     map.addLayer(drawnItems);

//     const drawControl = new L.Control.Draw({
//       edit: { featureGroup: drawnItems },
//       draw: { polygon: false, marker: false, circle: false, polyline: false, rectangle: true },
//     });
//     map.addControl(drawControl);

//     map.on(L.Draw.Event.CREATED, (event) => {
//       const layer = event.layer;
//       drawnItems.clearLayers();
//       drawnItems.addLayer(layer);
//       const bounds = layer.getBounds();
//       setSelectedArea({
//         bounds: [[bounds.getSouthWest().lat, bounds.getSouthWest().lng], [bounds.getNorthEast().lat, bounds.getNorthEast().lng]],
//         timestamp: new Date().toISOString(),
//       });
//     });

//     map.on(L.Draw.Event.DELETED, () => setSelectedArea(null));

//     return () => {
//       map.off(L.Draw.Event.CREATED);
//       map.off(L.Draw.Event.DELETED);
//       map.removeControl(drawControl);
//     };
//   }, [map, setSelectedArea]);

//   useEffect(() => {
//     if (visualization === 'heatmap' && selectedArea) {
//       if (heatmapLayer) map.removeLayer(heatmapLayer);
//       const points = generateHeatmapPoints(selectedArea.bounds); // Dummy data for now
//       const newHeatmap = L.heatLayer(points, { radius: 25 }).addTo(map);
//       setHeatmapLayer(newHeatmap);
//     } else if (heatmapLayer) {
//       map.removeLayer(heatmapLayer);
//       setHeatmapLayer(null);
//     }
//   }, [visualization, selectedArea, map]);

//   // Dummy function to generate heatmap points
//   const generateHeatmapPoints = (bounds) => {
//     const [sw, ne] = bounds;
//     const points = [];
//     for (let i = 0; i < 50; i++) {
//       const lat = sw[0] + Math.random() * (ne[0] - sw[0]);
//       const lng = sw[1] + Math.random() * (ne[1] - sw[1]);
//       points.push([lat, lng, Math.random()]);
//     }
//     return points;
//   };

//   return (
//     <>
//       <MapView location={location} mapStyle={mapStyle} onMapMove={onMapMove} />
//       {markers.map(marker => (
//         <Marker key={marker.id} position={[marker.lat, marker.lng]}>
//           <Popup>
//             <div>
//               <p>{new Date(marker.timestamp).toLocaleString()}</p>
//               <button
//                 className="btn btn-sm btn-danger"
//                 onClick={() => setMarkers(markers.filter(m => m.id !== marker.id))}
//               >
//                 Remove
//               </button>
//             </div>
//           </Popup>
//         </Marker>
//       ))}
//       {selectedArea && (
//         <Rectangle bounds={selectedArea.bounds} color="#ff0000" fillOpacity={0.1} />
//       )}
//     </>
//   );
// };

// const MapContainer = (props) => (
//   <LeafletMap
//     center={props.location}
//     zoom={13}
//     style={{ height: '85vh' }}
//     doubleClickZoom={false}
//     whenCreated={(map) => map.on('click', props.onMapClick)}
//   >
//     <MapContainerComponent {...props} />
//   </LeafletMap>
// );

// export default MapContainer;


import React, { useEffect, useState } from 'react';
import { MapContainer as LeafletMap, Marker, Popup, Rectangle, useMap } from 'react-leaflet';
import MapView from './MapView';
import 'leaflet/dist/leaflet.css';
import 'leaflet-draw/dist/leaflet.draw.css';
import L from 'leaflet';
import 'leaflet-draw';
import 'leaflet.heat';
import 'aframe';

const MapContainerComponent = ({ location, mapStyle, markers, setMarkers, selectedArea, setSelectedArea, onMapMove, onMapClick, visualization }) => {
  const map = useMap();
  const [heatmapLayer, setHeatmapLayer] = useState(null);
  const [arEnabled, setArEnabled] = useState(false);

  useEffect(() => {
    const drawnItems = new L.FeatureGroup();
    map.addLayer(drawnItems);

    const drawControl = new L.Control.Draw({
      edit: { featureGroup: drawnItems },
      draw: { polygon: false, marker: false, circle: false, polyline: false, rectangle: true },
    });
    map.addControl(drawControl);

    map.on(L.Draw.Event.CREATED, (event) => {
      const layer = event.layer;
      drawnItems.clearLayers();
      drawnItems.addLayer(layer);
      const bounds = layer.getBounds();
      setSelectedArea({
        bounds: [[bounds.getSouthWest().lat, bounds.getSouthWest().lng], [bounds.getNorthEast().lat, bounds.getNorthEast().lng]],
        timestamp: new Date().toISOString(),
      });
    });

    map.on(L.Draw.Event.DELETED, () => setSelectedArea(null));

    return () => {
      map.off(L.Draw.Event.CREATED);
      map.off(L.Draw.Event.DELETED);
      map.removeControl(drawControl);
    };
  }, [map, setSelectedArea]);

  useEffect(() => {
    if (visualization === 'heatmap' && selectedArea) {
      if (heatmapLayer) map.removeLayer(heatmapLayer);
      const points = generateHeatmapPoints(selectedArea.bounds);
      const newHeatmap = L.heatLayer(points, { radius: 25 }).addTo(map);
      setHeatmapLayer(newHeatmap);
    } else if (heatmapLayer) {
      map.removeLayer(heatmapLayer);
      setHeatmapLayer(null);
    }
  }, [visualization, selectedArea, map]);

  const generateHeatmapPoints = (bounds) => {
    const [sw, ne] = bounds;
    const points = [];
    for (let i = 0; i < 50; i++) {
      const lat = sw[0] + Math.random() * (ne[0] - sw[0]);
      const lng = sw[1] + Math.random() * (ne[1] - sw[1]);
      points.push([lat, lng, Math.random()]);
    }
    return points;
  };

  const enableAR = () => {
    setArEnabled(true);
    // Add A-Frame scene for AR
    const scene = document.createElement('a-scene');
    scene.setAttribute('arjs', 'trackingMethod: best; debugUIEnabled: false');
    
    const marker = document.createElement('a-marker');
    marker.setAttribute('preset', 'hiro');
    
    const box = document.createElement('a-box');
    box.setAttribute('position', '0 0.5 0');
    box.setAttribute('rotation', '0 45 0');
    box.setAttribute('color', '#4CC3D9');
    
    marker.appendChild(box);
    scene.appendChild(marker);
    document.body.appendChild(scene);
  };

  return (
    <>
      <MapView location={location} mapStyle={mapStyle} onMapMove={onMapMove} />
      {markers.map(marker => (
        <Marker key={marker.id} position={[marker.lat, marker.lng]}>
          <Popup>
            <div>
              <p>{new Date(marker.timestamp).toLocaleString()}</p>
              <button
                className="btn btn-sm btn-danger"
                onClick={() => setMarkers(markers.filter(m => m.id !== marker.id))}
              >
                Remove
              </button>
            </div>
          </Popup>
        </Marker>
      ))}
      {selectedArea && (
        <Rectangle bounds={selectedArea.bounds} color="#ff0000" fillOpacity={0.1} />
      )}
      <button onClick={enableAR} className="ar-button">Enable AR View</button>
    </>
  );
};

const MapContainer = (props) => (
  <LeafletMap
    center={props.location}
    zoom={13}
    style={{ height: '100%', width: '100%' }}
    doubleClickZoom={false}
    whenCreated={(map) => map.on('click', props.onMapClick)}
  >
    <MapContainerComponent {...props} />
  </LeafletMap>
);

export default MapContainer;
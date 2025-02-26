import React, { useEffect, useState } from 'react';
import { TileLayer, useMap, useMapEvents } from 'react-leaflet';

const MapView = ({ location, mapStyle, onMapMove }) => {
  const map = useMap();
  const [zoom, setZoom] = useState(13);

  useMapEvents({
    moveend: () => {
      const center = map.getCenter();
      onMapMove([center.lat, center.lng], map.getZoom());
    },
  });

  useEffect(() => {
    if (location) {
      map.setView(location, zoom);
    }
  }, [location, map, zoom]);

  return (
    <TileLayer url={mapStyle.url} attribution={mapStyle.attribution} />
  );
};

export default MapView;
import AnyMap from "anymap-ts";
import React, { useEffect, useRef } from "react";

const ParqueNorteViewer = () => {
  const mapRef = useRef(null);

  useEffect(() => {
    const map = new AnyMap.Map({
      container: mapRef.current,
      center: [40.478066, -3.653269],
      zoom: 12,
    });

    const layer = new AnyMap.TileLayer("https://www.example.com/parque-norte-ortofoto/{z}/{x}/{y}.tif");
    map.addLayer(layer);
  }, []);

  return <div ref={mapRef} style={{ height: 600, width: 800 }} />;
};

export default ParqueNorteViewer;

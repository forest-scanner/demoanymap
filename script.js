// script.js

import maplibregl from 'maplibre-gl';

maplibregl.accessToken = 'YOUR_MAPBOX_ACCESS_TOKEN'; // Replace with your Mapbox access token.

const map = new maplibregl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v12',
    center: [-4.7788, 36.7196],
    zoom: 15
});

map.on('load', () => {
    // Add a geojson source and layer here.
    // Example:
    // map.addSource('alcazaba', {
    //     type: 'geojson',
    //     data: './data/alcazaba.geojson'
    // });
    // map.addLayer({
    //     id: 'alcazaba-layer',
    //     type: 'fill',
    //     source: 'alcazaba',
    //     paint: {
    //         'fill-color': '#007cbf',
    //         'fill-opacity': 0.7
    //     }
    // });
});
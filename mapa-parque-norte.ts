// Mapa básico de AnyMap TS del Parque Norte de Madrid

// Importar librerías necesarias
import { AnyMap } from 'anymap-ts';

// Crear mapa
const mapa = new AnyMap('mapa', {
  center: [40.468326, -3.693048], // Coordenadas del Parque Norte de Madrid
  zoom: 15,
  basemap: 'OpenStreetMap'
});

// Agregar capas al mapa
mapa.addLayer('parque-norte', {
  type: 'geojson',
  data: {
    type: 'FeatureCollection',
    features: [
      {
        type: 'Feature',
        geometry: {
          type: 'Polygon',
          coordinates: [[
            [-3.694444, 40.467222],
            [-3.692778, 40.467222],
            [-3.692778, 40.469167],
            [-3.694444, 40.469167],
            [-3.694444, 40.467222]
          ]]
        },
        properties: {
          name: 'Parque Norte'
        }
      }
    ]
  }
});